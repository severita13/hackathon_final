from django.urls import path, include
from applications.post.views import PostDetailView , PostListView, PostCreateView, PostUpdateView, PostDeleteView, PostViewSet, PostLikeViewSet, SavedView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('', PostViewSet, )
router.register('', PostLikeViewSet)

urlpatterns = [
    path('post-list/<int:pk>/', PostDetailView.as_view()),
    path('post-list/', PostListView.as_view()),
    path('post-create/', PostCreateView.as_view()),
    path('post-update/<int:pk>/', PostUpdateView.as_view()),
    path('post-delete/<int:pk>/', PostDeleteView.as_view()),
    path('saved-list/', SavedView.as_view()),
    path('', include(router.urls)),
]

urlpatterns.extend(router.urls)