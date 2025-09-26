from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly  # Required import
from .models import Book
from .serializers import BookSerializer

# View to list all books
class BookListView(generics.ListAPIView):
    """
    GET: Retrieve a list of all books.
    Permissions: Accessible to all users (authenticated or unauthenticated).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Read-only for all users

# View to retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    """
    GET: Retrieve details of a specific book by ID.
    Permissions: Accessible to all users (authenticated or unauthenticated).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Read-only for all users

# View to create a new book
class BookCreateView(generics.CreateAPIView):
    """
    POST: Create a new book.
    Permissions: Restricted to authenticated users.
    Custom behavior: Ensures validated data is saved.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Write access for authenticated users

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
    permission_classes = [IsAuthenticated]  # Write access for authenticated users

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
    permission_classes = [IsAuthenticated]  # Write access for authenticated users