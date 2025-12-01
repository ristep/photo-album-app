from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from .views import AlbumViewSet, MediaFileViewSet, PublicMediaList

router = DefaultRouter()
router.register(r'albums', AlbumViewSet, basename='album')
router.register(r'media', MediaFileViewSet, basename='media')

urlpatterns = [
    # Keep the public endpoint before the router so 'public' is not
    # interpreted as a media PK by the router's detail route.
    path('media/public/', PublicMediaList.as_view(), name='public_media'),
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
