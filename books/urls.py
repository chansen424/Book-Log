from django.urls import path

from . import views

app_name = 'books'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:book_id>/', views.detail, name='detail'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_about_the_author', views.edit_about_the_author, name="edit_about_the_author")
]