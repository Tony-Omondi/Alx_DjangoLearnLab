from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)   # Book title
    author = models.CharField(max_length=100)  # Book author
    published_date = models.DateField(null=True, blank=True)  # Optional
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)  # Optional
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when added
    updated_at = models.DateTimeField(auto_now=True)      # Timestamp when updated

    def __str__(self):
        return f"{self.title} by {self.author}"
