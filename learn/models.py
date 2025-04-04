from django.db import models
from dictionary.models import Word

# Create your models here.
class Score(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    fail = models.IntegerField(default=0)
    success = models.IntegerField(default=0)
    last_try = models.DateField(auto_now=True)