

# View to list all books with filtering, searching, and ordering
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters  # Use filters alias for OrderingFilter and SearchFilter
from .models import Book
from .serializers import BookSerializer
from django_filters import rest_framework

# View to list all books with filtering, searching, and ordering
class BookListView(generics.ListAPIView):
    """
    GET: Retrieve a list of all books with filtering, searching, and ordering capabilities.
    Permissions: Accessible to all users (authenticated or unauthenticated).
    Filtering: Supports filtering by title, publication_year, and author.
    Searching: Supports text search on title and author name.
    Ordering: Supports ordering by title and publication_year (ascending or descending).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # Enable filtering, search, and ordering
    filterset_fields = ['title', 'publication_year', 'author']  # Fields for filtering
    search_fields = ['title', 'author__name']  # Fields for searching (title and author name)
    ordering_fields = ['title', 'publication_year']  # Fields for ordering
    ordering = ['title']  # Default ordering

# View to retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    """
    GET: Retrieve details of a specific book by ID.
    Permissions: Accessible to all users (authenticated or unauthenticated).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# View to create a new book
class BookCreateView(generics.CreateAPIView):
    """
    POST: Create a new book.
    Permissions: Restricted to authenticated users.
    Custom behavior: Ensures validated data is saved.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

# View to update an existing book
class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH: Update an existing book by ID.
    Permissions: Restricted to authenticated users.
    Custom behavior: Ensures validated data is saved.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()

# View to delete a book
class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE: Delete a book by ID.
    Permissions: Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]