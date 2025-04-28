from django.urls import path
from dictionary.views import create, read, delete, get_word_classes

urlpatterns = [
    path('new/', create, name='word-create'),
    path('', read, name='word-list'),
    path('delete/', delete, name='word-delete'),
    path('word_classes/', get_word_classes, name='word_classes')
]