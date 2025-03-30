from django.db import models

# Create your models here.

class Word(models.Model):
    french = models.CharField(max_length=100)
    korean = models.CharField(max_length=100)
    create_at = models.DateField(auto_now_add=True)
