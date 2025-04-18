from django.urls import path

from .views import create, read, update, delete

urlpatterns = [
    path('new/', create, name='word-create'),
    path('', read, name='word-list'),
    path('<int:pk>/edit/', update, name='word-update'),
    path('<int:pk>/delete/', delete, name='word-delete'),

]