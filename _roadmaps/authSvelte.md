Awesome — going with **JWT (JSON Web Tokens)** right away is a solid choice for scalability and modern API-based authentication. Let’s get you set up quickly and cleanly.

---

## 🔧 Step-by-Step Setup for JWT with Django + DRF

### 1. **Install the required packages**
```bash
pip install djangorestframework djangorestframework-simplejwt
```

---

### 2. **Update your `settings.py`**
Add apps if not already added:
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

Configure REST Framework to use JWT:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}
```

---

### 3. **Update `urls.py`**

In your main `urls.py` or a `urls.py` inside your API app:
```python
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

---

### 4. **Login from Svelte frontend**

```js
const login = async () => {
    const response = await fetch("http://localhost:8000/api/token/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username,
            password
        })
    });

    const data = await response.json();

    if (response.ok) {
        // Save tokens
        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);
        console.log("Logged in successfully!");
    } else {
        console.error("Login failed:", data);
    }
};
```

---

### 5. **Making Authenticated Requests**

Use the stored `access` token for protected routes:

```js
const token = localStorage.getItem("access");

const response = await fetch("http://localhost:8000/api/protected/", {
    headers: {
        "Authorization": `Bearer ${token}`
    }
});
```

---

### 6. **Protect Django views**

Make a protected view like this:
```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": f"Hello, {request.user.username}!"})
```

---

### 7. **Token Refresh (Optional)**

Use the `refresh` token to renew your access token when it expires:
```js
const refreshToken = localStorage.getItem("refresh");

const response = await fetch("http://localhost:8000/api/token/refresh/", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({ refresh: refreshToken })
});

const data = await response.json();

if (response.ok) {
    localStorage.setItem("access", data.access);
} else {
    console.error("Token refresh failed", data);
}
```

You can even automate this with interceptors or wrapper functions if you use a library like Axios (or a Svelte store).

---

## ✅ You're Good To Go!

From here, your auth stack is:
- Svelte handles UI, login, and stores tokens
- Django REST Framework with JWT handles auth and protects views
- You can later expand to include:
  - Token blacklisting
  - Password reset flows
  - User registration

---

Want help building the Svelte login store or setting up automatic token refreshing next?