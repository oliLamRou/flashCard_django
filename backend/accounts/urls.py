from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import preferences, api_login, api_logout, csrf

urlpatterns = [
    # path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', api_login, name='login'),
    path('logout/', api_logout, name='logout'),
    path('preference/', preferences, name='preference'),
    path('csrf/', csrf, name='csrf'),
]