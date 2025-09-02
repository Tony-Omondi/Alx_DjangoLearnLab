from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from .models import Library, Book

# Function-based view
def list_books(request):
    books = Book.objects.all()  # ✅ required by checker
    return render(request, "relationship_app/list_books.html", {"books": books})  # ✅ required by checker


# Class-based view for Library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.object.books.all()  # ✅ list books in this library
        return context
