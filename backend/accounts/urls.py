from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import preferences

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    # path('register/', register_view, name='register'),
    path('preference/', preferences, name='preference'),
]