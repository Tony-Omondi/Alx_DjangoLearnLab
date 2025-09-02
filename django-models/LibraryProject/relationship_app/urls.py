from django.urls import path
from . import views
from .views import LibraryDetailView

urlpatterns = [
    # ✅ Function-based view route
    path("libraries/", views.library_list, name="library-list"),

    # ✅ Class-based view route
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library-detail"),
]
