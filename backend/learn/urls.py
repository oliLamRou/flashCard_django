from django.urls import path

from .views import guess, score

urlpatterns = [
    path('guess/', guess, name='guess'),
    path('score/', score, name='score')
]