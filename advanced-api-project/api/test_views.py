from rest_framework.test import APITestCase  # Required import
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Author, Book
from api.serializers import BookSerializer
from datetime import datetime

class BookAPITests(APITestCase):
    """
    Test suite for Book model API endpoints.
    Tests CRUD operations, filtering, searching, ordering, and permissions.
    """
    def setUp(self):
        """
        Set up test data and client before each test.
        Creates a user, author, and two books for testing.
        """
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book1 = Book.objects.create(
            title="Harry Potter", publication_year=1997, author=self.author
        )
        self.book2 = Book.objects.create(
            title="New Book", publication_year=2023, author=self.author
        )
        self.valid_book_data = {
            'title': 'Another Book',
            'publication_year': 2020,
            'author': self.author.id
        }
        self.invalid_book_data = {
            'title': 'Future Book',
            'publication_year': datetime.now().year + 1,  # Future year
            'author': self.author.id
        }

    def test_list_books(self):
        """
        Test GET /api/books/ to list all books.
        Should return 200 OK and correct book data.
        """
        response = self.client.get('/api/books/')
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_book(self):
        """
        Test GET /api/books/<id>/ to retrieve a single book.
        Should return 200 OK and correct book data.
        """
        response = self.client.get(f'/api/books/{self.book1.id}/')
        serializer = BookSerializer(self.book1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book_authenticated(self):
        """
        Test POST /api/books/create/ with authenticated user.
        Should return 201 Created and correct book data.
        """
        self.client.login(username='testuser', password='testpass123')  # Use login
        response = self.client.post('/api/books/create/', self.valid_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)  # Two initial books + new one
        self.assertEqual(response.data['title'], self.valid_book_data['title'])
        self.client.logout()

    def test_create_book_unauthenticated(self):
        """
        Test POST /api/books/create/ without authentication.
        Should return 403 Forbidden.
        """
        response = self.client.post('/api/books/create/', self.valid_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_invalid_data(self):
        """
        Test POST /api/books/create/ with invalid data (future publication year).
        Should return 400 Bad Request.
        """
        self.client.login(username='testuser', password='testpass123')  # Use login
        response = self.client.post('/api/books/create/', self.invalid_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
        self.client.logout()

    def test_update_book_authenticated(self):
        """
        Test PUT /api/books/update/<id>/ with authenticated user.
        Should return 200 OK and updated book data.
        """
        self.client.login(username='testuser', password='testpass123')  # Use login
        updated_data = {
            'title': 'Updated Harry Potter',
            'publication_year': 1998,
            'author': self.author.id
        }
        response = self.client.put(f'/api/books/update/{self.book1.id}/', updated_data, format='json')
        self.book1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.book1.title, updated_data['title'])
        self.assertEqual(self.book1.publication_year, updated_data['publication_year'])
        self.client.logout()

    def test_update_book_unauthenticated(self):
        """
        Test PUT /api/books/update/<id>/ without authentication.
        Should return 403 Forbidden.
        """
        updated_data = {
            'title': 'Updated Harry Potter',
            'publication_year': 1998,
            'author': self.author.id
        }
        response = self.client.put(f'/api/books/update/{self.book1.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_authenticated(self):
        """
        Test DELETE /api/books/delete/<id>/ with authenticated user.
        Should return 204 No Content and remove the book.
        """
        self.client.login(username='testuser', password='testpass123')  # Use login
        response = self.client.delete(f'/api/books/delete/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)  # One book left
        self.client.logout()

    def test_delete_book_unauthenticated(self):
        """
        Test DELETE /api/books/delete/<id>/ without authentication.
        Should return 403 Forbidden.
        """
        response = self.client.delete(f'/api/books/delete/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_by_title(self):
        """
        Test filtering books by title (/api/books/?title=Harry%20Potter).
        Should return 200 OK and filtered book data.
        """
        response = self.client.get('/api/books/?title=Harry Potter')
        books = Book.objects.filter(title='Harry Potter')
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_by_publication_year(self):
        """
        Test filtering books by publication_year (/api/books/?publication_year=1997).
        Should return 200 OK and filtered book data.
        """
        response = self.client.get('/api/books/?publication_year=1997')
        books = Book.objects.filter(publication_year=1997)
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_by_author(self):
        """
        Test filtering books by author (/api/books/?author=1).
        Should return 200 OK and filtered book data.
        """
        response = self.client.get(f'/api/books/?author={self.author.id}')
        books = Book.objects.filter(author=self.author)
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_search_by_title(self):
        """
        Test searching books by title (/api/books/?search=Potter).
        Should return 200 OK and matching book data.
        """
        response = self.client.get('/api/books/?search=Potter')
        books = Book.objects.filter(title__icontains='Potter')
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_search_by_author_name(self):
        """
        Test searching books by author name (/api/books/?search=Rowling).
        Should return 200 OK and matching book data.
        """
        response = self.client.get('/api/books/?search=Rowling')
        books = Book.objects.filter(author__name__icontains='Rowling')
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_order_by_title(self):
        """
        Test ordering books by title (/api/books/?ordering=title).
        Should return 200 OK and books sorted by title.
        """
        response = self.client.get('/api/books/?ordering=title')
        books = Book.objects.order_by('title')
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_order_by_publication_year_desc(self):
        """
        Test ordering books by publication_year descending (/api/books/?ordering=-publication_year).
        Should return 200 OK and books sorted by publication_year (descending).
        """
        response = self.client.get('/api/books/?ordering=-publication_year')
        books = Book.objects.order_by('-publication_year')
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)