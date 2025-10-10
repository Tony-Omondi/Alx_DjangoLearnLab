from rest_framework import viewsets, permissions, generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User = get_user_model()


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
        post = serializer.save(author=self.request.user)
        # Notify followers of new post
        for follower in self.request.user.followers.all():
            Notification.objects.create(
                recipient=follower,
                actor=self.request.user,
                verb='posted',
                target=post,
                target_content_type=ContentType.objects.get_for_model(Post)
            )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = None  # Configured globally in settings.py

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        # Notify post author of new comment
        if comment.post.author != self.request.user:
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb='commented on',
                target=comment.post,
                target_content_type=ContentType.objects.get_for_model(Post)
            )


class LikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({'error': 'You already liked this post'}, status=status.HTTP_400_BAD_REQUEST)

        # Notify post author of new like
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked',
                target=post,
                target_content_type=ContentType.objects.get_for_model(Post)
            )
        return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)


class UnlikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response({'error': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        return Response({'message': 'Like removed'}, status=status.HTTP_200_OK)


class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request):
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data)
