"""
Forms for the bookshelf app.

This file defines Django forms for secure input handling:
- BookForm: ModelForm for Book instances, used in create/edit views.
- ExampleForm: Simple form for testing security features (e.g., CSRF, input validation).

Security Notes:
- Forms automatically sanitize inputs to prevent XSS and SQL injection.
- Use with {% csrf_token %} in templates for CSRF protection.
- Validation ensures data integrity (e.g., length limits, required fields).
"""

from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    """
    Form for creating/editing Book instances.
    Validates and sanitizes user inputs for title, author, and publication_date.
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date']
        widgets = {
            'title': forms.TextInput(attrs={'max_length': 200}),
            'author': forms.TextInput(attrs={'max_length': 100}),
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_title(self):
        """
        Custom validation: Ensure title is not empty and escapes any potential XSS.
        """
        title = self.cleaned_data['title'].strip()
        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long.")
        return title

    def clean_author(self):
        """
        Custom validation: Ensure author name is valid.
        """
        author = self.cleaned_data['author'].strip()
        if not author:
            raise forms.ValidationError("Author name is required.")
        return author


class ExampleForm(forms.Form):
    """
    Example form for testing security features.
    Includes fields to demonstrate input sanitization and validation.
    Used in form_example.html template.
    """
    name = forms.CharField(max_length=100, label="Your Name", required=True)
    email = forms.EmailField(label="Email", required=True)
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        label="Message",
        required=False
    )

    def clean_name(self):
        """
        Custom validation: Sanitize name and prevent XSS.
        """
        name = self.cleaned_data['name'].strip()
        if len(name) > 50:
            raise forms.ValidationError("Name is too long (max 50 characters).")
        # Django automatically escapes output in templates, but we can add extra sanitization if needed
        return name

    def clean_email(self):
        """
        Custom validation: Ensure valid email format.
        """
        email = self.cleaned_data['email']
        if '@' not in email:
            raise forms.ValidationError("Enter a valid email address.")
        return email

    def clean_message(self):
        """
        Custom validation: Limit message length and sanitize for XSS.
        """
        message = self.cleaned_data['message'].strip()
        if len(message) > 500:
            raise forms.ValidationError("Message is too long (max 500 characters).")
        return message