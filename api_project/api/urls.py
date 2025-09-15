from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

# Create router and register ViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

# URL patterns
urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),  # Existing ListAPIView (optional)
    path('', include(router.urls)),  # Includes all CRUD routes for BookViewSet
]
