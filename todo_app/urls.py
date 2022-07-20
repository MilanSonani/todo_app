from django.urls import path
from .views import UserRegisterView, UserLoginView, ChangePasswordView, AddBookView, UpdateBookView, DeleteBookView, DetailBookView, ListBookView

urlpatterns = [
    path('register/', UserRegisterView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('add-book/', AddBookView.as_view()),
    path('book-list/', ListBookView.as_view()),
    path('book-detail/<int:pk>/', DetailBookView.as_view()),
    path('update-book/<int:pk>/', UpdateBookView.as_view()),
    path('delete-book/<int:pk>/', DeleteBookView.as_view()),
    path('change_password/<int:pk>/', ChangePasswordView.as_view()),
]