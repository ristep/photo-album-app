from rest_framework import serializers
from .models import Album, MediaFile

class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = ('id', 'owner', 'file', 'original_filename', 'media_type', 'width', 'height', 'duration', 'uploaded_at', 'taken_at', 'metadata', 'is_favorite', 'is_archived')

class AlbumSerializer(serializers.ModelSerializer):
    media = MediaFileSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ('id', 'title', 'description', 'owner', 'is_public', 'created_at', 'updated_at', 'media')
        read_only_fields = ('owner',)
