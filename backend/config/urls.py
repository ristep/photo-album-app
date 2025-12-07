from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.albums.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
