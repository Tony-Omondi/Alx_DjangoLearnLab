from django.contrib import admin
from .models import Author, Book

# Register models to manage them via Django admin
admin.site.register(Author)
admin.site.register(Book)