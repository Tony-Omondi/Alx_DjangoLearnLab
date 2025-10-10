from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'content']
    filterset_fields = ['title', 'content']
    pagination_class = None  # Configured globally in settings.py

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = None  # Configured globally in settings.py

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request):
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data)
