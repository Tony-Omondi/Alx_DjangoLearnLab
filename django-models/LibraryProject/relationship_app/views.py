from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Library, Book

# Function-based view for listing all libraries (already exists if you added it earlier)
def library_list(request):
    libraries = Library.objects.all()
    return render(request, "relationship_app/library_list.html", {"libraries": libraries})


# ✅ Class-based view for library details with books
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # include books in this library
        context["books"] = Book.objects.filter(library=self.object)
        return context
