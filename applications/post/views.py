import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from applications.post.models import Post, Saved
from applications.post.serializers import *
from applications.post.permissions import IsPostAuthor
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import get_object_or_404


class PostFilter(django_filters.FilterSet):
    author = django_filters.NumberFilter(field_name='id')

    class Meta:
        model = Post
        fields = [ ]


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, ]
    filter_class = PostFilter
    search_fields = ['title', ]

    def get_serializer_context(self):
        return {'request': self.request}


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]


class PostUpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsPostAuthor]


class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsPostAuthor]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = []
        elif self.action == 'save_post':
            permissions = [IsAuthenticated, ]
        else:
            permissions = [IsPostAuthor, ]
        return [permissions() for permissions in permissions]


    @action(detail=True, methods=['POST'])
    def saved(self, requests, *args, **kwargs):
        post = self.get_object()
        saved_obj, _ = Saved.objects.get_or_create(post=post, user=requests.user)
        saved_obj.saved = not saved_obj.saved
        saved_obj.save()
        status = 'Сохранено в избранные'
        if not saved_obj.saved:
            status = 'Удалено из избранных'
        return Response({'status': status})

    def get_serializer_context(self):
        return {'request': self.request}


class PostLikeViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = []
        elif self.action == 'like':
            permissions = [IsAuthenticated, ]
        else:
            permissions = [IsPostAuthor, ]
        return [permissions() for permissions in permissions]


    # @login_required
    # def like(request):
    #     if request.POST.get('action') == 'post':
    #         result = ''
    #         id = int(request.POST.get('postid'))
    #         post = get_object_or_404(Post, id=id)
    #         if post.likes.filter(id=request.user.id).exists():
    #             post.likes.remove(request.user)
    #             post.like_count -= 1
    #             result = post.like_count
    #             post.save
    #         else:
    #             post.likes.add(request.user)
    #             post.like_count += 1
    #             result = post.like.count
    #         return Response({'result':result})

    @action(detail=True, methods=['POST'])
    def like(self, requests, *args, **kwargs):
        post = self.get_object()
        like_obj, _ = Like.objects.get_or_create(post=post, user=requests.user)
        like_obj.like = not like_obj.like
        like_obj.save()
        status = 'Liked'
        if not like_obj.like:
            status = 'Unliked'
        return Response({'status': status})

    def get_serializer_context(self):
        return {'request': self.request}


class SavedView(generics.ListAPIView):
    queryset = Saved.objects.all()
    serializer_class = SavedSerializer


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer