from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# Function-based view to list all books
def list_books(request):
    try:
        books = Book.objects.all()
        return render(request, 'relationship_app/list_books.html', {'books': books})
    except Exception as e:
        return render(request, 'relationship_app/error.html', {'error': str(e)})

# Class-based view to display library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['books'] = self.object.books.all()
        except Exception as e:
            context['error'] = f"Error retrieving books: {str(e)}"
        return context