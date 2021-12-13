from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

# from applications.post.views import PostViewSet
# from applications.review.views import ReviewViewSet
# from applications.account.views import UsersListViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Authentication API",
        default_version='v1',
        description='Test Description'
    ),
    public=True
)

# router = DefaultRouter()
# router.register('reviews', ReviewViewSet)
# router.register('posts', PostViewSet)

urlpatterns = [
    path('swagger/', schema_view.with_ui()),
    path('admin/', admin.site.urls),
    path('account/', include('applications.account.urls')),
    path('post/', include('applications.post.urls')),
    path('review/', include('applications.review.urls')),
    path('', include('applications.celery.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)