from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('post/<int:post_id>/comments/new/', views.CommentCreateView.as_view(), name='comment_new'),
    path('post/<int:post_id>/comments/<int:comment_id>/edit/', views.CommentUpdateView.as_view(), name='comment_edit'),
    path('post/<int:post_id>/comments/<int:comment_id>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
]