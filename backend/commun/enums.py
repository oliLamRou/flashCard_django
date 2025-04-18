from django.db import models

class LANGUAGE(models.TextChoices):
    FR = 'FR', 'Français'
    EN = 'EN', 'English'
    KR = 'KR', '한국어'