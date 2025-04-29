from django.urls import path
from accounts.views import preferences, register

urlpatterns = [
    # path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('login/', api_login, name='login'),
    # path('logout/', api_logout, name='logout'),
    # path('csrf/', csrf, name='csrf'),
    path('register/', register, name='register'),
    path('preference/', preferences, name='preference'),
]