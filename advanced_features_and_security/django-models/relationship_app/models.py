from django.db import models

# =======================
# Author Model
# =======================
class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="Author Name")
    bio = models.TextField(blank=True, null=True, verbose_name="Biography")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# =======================
# Book Model
# =======================
from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]

    def __str__(self):
        return self.title



# =======================
# Library Model
# =======================
class Library(models.Model):
    name = models.CharField(max_length=150, verbose_name="Library Name")
    books = models.ManyToManyField(
        Book, 
        related_name="libraries", 
        blank=True,
        verbose_name="Books in Library"
    )
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# =======================
# Librarian Model
# =======================
class Librarian(models.Model):
    name = models.CharField(max_length=100, verbose_name="Librarian Name")
    library = models.OneToOneField(
        Library, 
        on_delete=models.CASCADE, 
        related_name="librarian", 
        verbose_name="Library"
    )
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.library.name})"
