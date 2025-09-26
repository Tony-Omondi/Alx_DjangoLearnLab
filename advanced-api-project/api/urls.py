from django.urls import path
from .views import BookListCreateView, BookDetailView

# URL patterns for Book-related endpoints
urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),  # List and create books
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),  # Retrieve, update, delete a book
]