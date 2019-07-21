from django.urls import path

from . import views

app_name = 'books'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:book_id>/', views.detail, name='detail'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_about_the_author', views.edit_about_the_author, name="edit_about_the_author"),
    path('edit_isbn', views.edit_isbn, name="edit_isbn"),
    path('add_to_favorites', views.add_to_favorites, name="add_to_favorites"),
    path('remove_from_favorites', views.remove_from_favorites, name="remove_from_favorites"),

]