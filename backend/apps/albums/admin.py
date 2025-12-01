from django.contrib import admin
from .models import Album, MediaFile, AlbumMedia

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'created_at')

@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'media_type', 'owner', 'uploaded_at')

@admin.register(AlbumMedia)
class AlbumMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'album', 'media', 'added_at')
    list_filter = ('album', 'added_at')
