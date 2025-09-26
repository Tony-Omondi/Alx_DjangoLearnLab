from django.db import models

# Author model to store author information
class Author(models.Model):
    name = models.CharField(max_length=100)  # Author's name, e.g., "J.K. Rowling"

    def __str__(self):
        return self.name

# Book model to store book information with a relationship to Author
class Book(models.Model):
    title = models.CharField(max_length=200)  # Book's title, e.g., "Harry Potter"
    publication_year = models.IntegerField()  # Year of publication, e.g., 1997
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')  # One-to-many relationship with Author

    def __str__(self):
        return self.title