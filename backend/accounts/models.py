from django.db import models
from django.contrib.auth.models import User
from commun.enums import LANGUAGE

class Preference(models.Model):
    class LEARN_MODE(models.TextChoices):
        normal = 'NORMAL'
        reversed = 'REVERSED'

    class LEARN_DECK(models.TextChoices):
        all = 'ALL', 'Created By Everyone',
        user = 'USER', 'Created By Me',
        favorite = 'FAVORITE', 'My Favorite'
        
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    languageA = models.CharField(max_length=20, choices=LANGUAGE, default=LANGUAGE.FR)
    languageB = models.CharField(max_length=20, choices=LANGUAGE, default=LANGUAGE.KR)
    learnMode = models.CharField(max_length=100, choices=LEARN_MODE ,default=LEARN_MODE.normal)
    learnDeck = models.CharField(max_length=100, choices=LEARN_DECK, default=LEARN_DECK.all)
    learnUserWordsPerc = models.FloatField(default=1)
    learnFavoriteWordsPerc = models.FloatField(default=0.01)
    learnNewWordsPerc = models.FloatField(default=1)
    learnFailWordsPerc = models.FloatField(default=0.01)
    learnSuccessWordsPerc = models.FloatField(default=0.01)


    def __str__(self):
        language = f"{self.user.username}'s languages: {self.languageA} → {self.languageB}"
        return language