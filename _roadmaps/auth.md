Awesome! Here's a clean, minimal Django `auth` app setup with:

- ✅ Registration
- ✅ Login
- ✅ Logout
- ✅ Password hashing
- ✅ Simple redirect after login
- ✅ Using Django's built-in User model

---

### 🔧 Step 1: Create an `authapp` (or call it `accounts`, `users`, etc.)

```bash
python manage.py startapp authapp
```

---

### 🧩 Step 2: `authapp/forms.py`

```python
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
```

---

### 📄 Step 3: `authapp/views.py`

```python
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegisterForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # or 'dashboard' or wherever
    else:
        form = RegisterForm()
    return render(request, 'authapp/register.html', {'form': form})
```

---

### 🧭 Step 4: `authapp/urls.py`

```python
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register_view

urlpatterns = [
    path('login/', LoginView.as_view(template_name='authapp/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register_view, name='register'),
]
```

---

### 🗺️ Step 5: Add to your **project-level** `urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authapp.urls')),  # <--- include your auth app URLs
    path('', include('mainapp.urls')),       # your other stuff
]
```

---

### 🎨 Step 6: Templates

#### `templates/authapp/login.html`

```html
<h2>Login</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Login</button>
</form>
<a href="{% url 'register' %}">Register</a>
```

#### `templates/authapp/register.html`

```html
<h2>Register</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Register</button>
</form>
<a href="{% url 'login' %}">Already have an account?</a>
```

---

### ⚙️ Step 7: Settings

In `settings.py`:

```python
LOGIN_REDIRECT_URL = '/'          # where to go after login
LOGOUT_REDIRECT_URL = '/auth/login/'  # after logout

# Templating config (if not already set)
TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']
```

---

✅ Boom! You now have a fully working auth system with:

- `/auth/login/`
- `/auth/logout/`
- `/auth/register/`

Let me know if you want to add password reset via email or make this API-friendly with Django REST Framework.