# query_samples.py

from relationship_app.models import Author, Book, Library, Librarian

# Sample queries

# 1. Create Authors
author1 = Author.objects.create(name="Chinua Achebe")
author2 = Author.objects.create(name="Ngũgĩ wa Thiong'o")

# 2. Create Books
book1 = Book.objects.create(title="Things Fall Apart", author=author1)
book2 = Book.objects.create(title="The River Between", author=author2)

# 3. Create Library
library = Library.objects.create(name="Nairobi Public Library")

# 4. Add books to library (Many-to-Many relationship)
library.books.add(book1, book2)

# 5. Create Librarian
librarian = Librarian.objects.create(name="Mary Wanjiku", library=library)

# 6. Queries
print("All Authors:", Author.objects.all())
print("All Books:", Book.objects.all())
print("Books in Library:", library.books.all())
print("Librarian for Library:", library.librarian.name)
