from rest_framework import viewsets, permissions, generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import PermissionDenied
from .models import Album, MediaFile, AlbumMedia
from .serializers import AlbumSerializer, MediaFileSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Album.objects.filter(owner=self.request.user)
        return Album.objects.none()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MediaFileViewSet(viewsets.ModelViewSet):
    serializer_class = MediaFileSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return MediaFile.objects.filter(owner=self.request.user)
        return MediaFile.objects.none()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PublicMediaList(generics.ListAPIView):
    """List media files that belong to public albums.

    This endpoint is public (AllowAny) and returns distinct media files
    that are associated with an Album where `is_public=True`.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = MediaFileSerializer

    def get_queryset(self):
        return MediaFile.objects.filter(album_media__album__is_public=True).distinct()
