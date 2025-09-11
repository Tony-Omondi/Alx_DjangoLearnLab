from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseBadRequest
from .models import Book
from .forms import BookForm, ExampleForm  # Added ExampleForm import
from .forms import ExampleForm

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    # Safe ORM query, no raw SQL
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
    # Safe retrieval using get_object_or_404
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():  # Validates and sanitizes input
            form.save()
            return redirect('book_list')
        else:
            return render(request, 'bookshelf/book_form.html', {'form': form}, status=400)
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():  # Validates and sanitizes input
            form.save()
            return redirect('book_list')
        else:
            return render(request, 'bookshelf/book_form.html', {'form': form}, status=400)
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form})

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

@permission_required('bookshelf.can_view', raise_exception=True)
def book_search(request):
    query = request.GET.get('q', '')
    if len(query) > 100:  # Basic input length validation
        return HttpResponseBadRequest("Search query too long")
    # Safe ORM query with parameterization
    books = Book.objects.filter(title__icontains=query)
    return render(request, 'bookshelf/book_list.html', {'books': books, 'query': query})

@permission_required('bookshelf.can_view', raise_exception=True)
def example_view(request):
    """
    View for handling ExampleForm submissions.
    Demonstrates secure form handling with CSRF protection and input validation.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process cleaned data securely (e.g., log or save to database)
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # For demo purposes, redirect to book_list
            return redirect('book_list')
        else:
            return render(request, 'bookshelf/form_example.html', {'form': form}, status=400)
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})