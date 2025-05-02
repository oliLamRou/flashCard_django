from django.urls import path
from accounts.views import preferences, register, login, refresh_tokens, user_info

urlpatterns = [
    path('login/', login, name='login'),
    path('refresh/', refresh_tokens, name='refresh'),
    path('register/', register, name='register'),
    path('preference/', preferences, name='preference'),
    path('info/', user_info, name='info'),
]