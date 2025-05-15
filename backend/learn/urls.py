from django.urls import path

from .views import guess, score, archive

urlpatterns = [
    path('guess/', guess, name='guess'),
    path('score/', score, name='score'),
    path('archive/', archive, name='archive'),
]