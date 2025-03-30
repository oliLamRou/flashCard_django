Django does not have a **default form template** like how some frontend frameworks provide ready-made UI components. However, it has **Django Forms**, which generate HTML form fields automatically. You can use these forms in templates to create a CRUD interface for adding new words.

---

## Steps to Create a Simple CRUD App for "Words"

### 1️⃣ Create a Model (`models.py`)
Define a `Word` model in `learn/models.py`:

```python
from django.db import models

class Word(models.Model):
    term = models.CharField(max_length=100)
    definition = models.TextField()

    def __str__(self):
        return self.term
```

Run migrations to apply this model:

```sh
python manage.py makemigrations
python manage.py migrate
```

---

### 2️⃣ Create a Form (`forms.py`)
In the `learn` app, create a `forms.py` file and define a Django form:

```python
from django import forms
from .models import Word

class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['term', 'definition']
```

This form will automatically generate HTML fields for `term` and `definition`.

---

### 3️⃣ Create Views (`views.py`)
Modify `learn/views.py` to handle CRUD operations.

```python
from django.shortcuts import render, redirect, get_object_or_404
from .models import Word
from .forms import WordForm

# List all words
def word_list(request):
    words = Word.objects.all()
    return render(request, 'learn/word_list.html', {'words': words})

# Create a new word
def word_create(request):
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('word-list')
    else:
        form = WordForm()
    return render(request, 'learn/word_form.html', {'form': form})

# Update an existing word
def word_update(request, pk):
    word = get_object_or_404(Word, pk=pk)
    if request.method == 'POST':
        form = WordForm(request.POST, instance=word)
        if form.is_valid():
            form.save()
            return redirect('word-list')
    else:
        form = WordForm(instance=word)
    return render(request, 'learn/word_form.html', {'form': form})

# Delete a word
def word_delete(request, pk):
    word = get_object_or_404(Word, pk=pk)
    if request.method == 'POST':
        word.delete()
        return redirect('word-list')
    return render(request, 'learn/word_confirm_delete.html', {'word': word})
```

---

### 4️⃣ Create Templates (`templates/learn/`)

#### 📌 `word_list.html` (List Words)
```html
<h1>Word List</h1>
<a href="{% url 'word-create' %}">Add New Word</a>
<ul>
    {% for word in words %}
        <li>
            {{ word.term }} - {{ word.definition }}
            <a href="{% url 'word-update' word.pk %}">Edit</a>
            <a href="{% url 'word-delete' word.pk %}">Delete</a>
        </li>
    {% endfor %}
</ul>
```

#### 📌 `word_form.html` (Create/Edit Word)
```html
<h1>{% if form.instance.pk %}Edit{% else %}Add{% endif %} Word</h1>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
</form>
<a href="{% url 'word-list' %}">Back to List</a>
```

#### 📌 `word_confirm_delete.html` (Confirm Delete)
```html
<h1>Delete Word</h1>
<p>Are you sure you want to delete "{{ word.term }}"?</p>
<form method="post">
    {% csrf_token %}
    <button type="submit">Yes, delete</button>
</form>
<a href="{% url 'word-list' %}">Cancel</a>
```

---

### 5️⃣ Define URLs (`urls.py`)
In `learn/urls.py`, define routes for CRUD operations:

```python
from django.urls import path
from .views import word_list, word_create, word_update, word_delete

urlpatterns = [
    path('', word_list, name='word-list'),
    path('new/', word_create, name='word-create'),
    path('<int:pk>/edit/', word_update, name='word-update'),
    path('<int:pk>/delete/', word_delete, name='word-delete'),
]
```

---

### 6️⃣ Register the App URLs in Project (`project/urls.py`)
Make sure the project-level `urls.py` includes the `learn` app:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('learn/', include('learn.urls')),  # Include learn app
]
```

---

### 7️⃣ Run the Server and Test 🚀
```sh
python manage.py runserver
```
Visit `http://127.0.0.1:8000/learn/` to manage words!

---
### ✅ Summary
- **Django Forms** auto-generate form fields.
- **Templates (`.as_p`)** display the form automatically.
- **CRUD views** handle adding, updating, and deleting words.
- **CSRF tokens** ensure security in forms.

Let me know if you want to improve the UI with Django's built-in `admin`, Bootstrap, or JavaScript! 🚀