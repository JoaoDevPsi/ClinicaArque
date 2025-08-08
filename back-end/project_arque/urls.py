from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from content_manager.views import ArticleViewSet, GalleryPostViewSet
from contact_form.views import ContactSubmissionCreateView
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'gallery-posts', GalleryPostViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/contact/', ContactSubmissionCreateView.as_view(), name='contact_submit'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)