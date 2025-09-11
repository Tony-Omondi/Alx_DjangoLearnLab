from .views import list_books
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Function-based and class-based views
    path("books/", views.list_books, name="list_books"),
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),

    # 🔑 Authentication URLs
    path("register/", views.register_view, name="register"),
    path(
        "login/",
        LoginView.as_view(template_name="relationship_app/login.html"),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(template_name="relationship_app/logout.html"),
        name="logout",
    ),

    # 📘 Book management views with permissions
    path("add_book/", views.add_book_view, name="add_book"),
    path("edit_book/", views.edit_book_view, name="edit_book"),
    path("delete_book/", views.delete_book_view, name="delete_book"),

    # 👥 Role-based views
    path("admin-view/", views.admin_view, name="admin_view"),
    path("librarian-view/", views.librarian_view, name="librarian_view"),
    path("member-view/", views.member_view, name="member_view"),
]

