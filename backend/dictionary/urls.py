from django.urls import path
from dictionary.views import create, read, update, delete, get_word_classes

urlpatterns = [
    path('new/', create, name='word-create'),
    path('', read, name='word-list'),
    path('<int:pk>/edit/', update, name='word-update'),
    path('delete/', delete, name='word-delete'),
    path('word_classes/', get_word_classes, name='word_classes')
]