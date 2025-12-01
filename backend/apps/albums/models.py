from django.db import models
from django.conf import settings
from django.utils import timezone
import os
import uuid
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models.signals import post_save
from django.dispatch import receiver

User = settings.AUTH_USER_MODEL


def media_upload_to(instance, filename):
    """Upload initially to a temporary name. After the model is saved the
    post_save signal will rename the file to `media/{id}{ext}` so all media
    live in a single folder with a name based on the DB id.
    """
    base, ext = os.path.splitext(filename)
    return f"tmp_{uuid.uuid4().hex}{ext}"

class Album(models.Model):
    owner = models.ForeignKey(User, related_name='albums', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"

class MediaFile(models.Model):
    MEDIA_TYPE_CHOICES = (
        ('photo', 'Photo'),
        ('video', 'Video'),
    )
    owner = models.ForeignKey(User, related_name='mediafiles', on_delete=models.CASCADE)
    file = models.FileField(upload_to=media_upload_to)
    original_filename = models.CharField(max_length=500, blank=True, help_text="Original filename uploaded by user")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    taken_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    is_favorite = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.file.name}"


# After saving a MediaFile we want the file name to be deterministic and
# based on the model id. We move the uploaded file from the temporary name
# to `media/{id}{ext}` and update the FileField.
@receiver(post_save, sender=MediaFile)
def _mediafile_rename_on_save(sender, instance, created, **kwargs):
    # Skip if already processed (recursive call protection)
    if getattr(instance, '_skip_rename_signal', False):
        return

    # No file to process
    if not instance.file:
        return

    current_name = instance.file.name
    filename_only = os.path.basename(current_name)
    
    # Store original filename if not already set (extract from current path)
    if not instance.original_filename:
        instance.original_filename = filename_only

    # Ensure extension preserved
    _, ext = os.path.splitext(current_name)
    desired_name = f"{instance.id}{ext}"

    # If already correct, nothing to do
    if current_name == desired_name:
        # Still save original_filename if it was just set
        if instance.original_filename and instance.original_filename != filename_only:
            return
        # Mark as skip to prevent infinite loop
        instance._skip_rename_signal = True
        instance.save(update_fields=['original_filename'])
        instance._skip_rename_signal = False
        return

    try:
        # Read current file and write to the new path
        with default_storage.open(current_name, 'rb') as f:
            content = f.read()

        # Save the content under the desired name
        default_storage.save(desired_name, ContentFile(content))

        # Delete the old temporary file
        try:
            default_storage.delete(current_name)
        except Exception:
            pass

        # Update the model's FileField (this will not loop because name now matches)
        instance.file.name = desired_name
        # Mark as skip to prevent recursive signal
        instance._skip_rename_signal = True
        instance.save(update_fields=['file'])
        instance._skip_rename_signal = False
    except Exception:
        # If anything goes wrong, don't break the request — leave the original file.
        return


class AlbumMedia(models.Model):
    """
    Through model for many-to-many relationship between Album and MediaFile.
    Allows a media file to belong to multiple albums.
    """
    album = models.ForeignKey(Album, related_name='album_media', on_delete=models.CASCADE)
    media = models.ForeignKey(MediaFile, related_name='album_media', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('album', 'media')
        verbose_name_plural = "Album Media"

    def __str__(self):
        return f"{self.album.title} - {self.media.file.name}"
