from django.db import models
from django.contrib.auth.models import User
from commun.enums import LANGUAGE

class Preference(models.Model):
    class LEARN_MODE(models.TextChoices):
        normal = 'NORMAL'
        reversed = 'REVERSED'
        
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    languageA = models.CharField(max_length=20, choices=LANGUAGE, default=LANGUAGE.FR)
    languageB = models.CharField(max_length=20, choices=LANGUAGE, default=LANGUAGE.KR)
    learnMode = models.CharField(max_length=100, choices=LEARN_MODE ,default=LEARN_MODE.normal)

    def __str__(self):
        return f"{self.user.username}'s preferences: {self.languageA} → {self.languageB}"