import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flashcard.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Preference
from dictionary.models import Word
from learn.models import Score

score = Score.objects.all().first()
# user = User.objects.filter(username='userA').first()
# word = Word.objects.filter(id=10).first()

# x = Score.objects.filter(user=user, word=word).first()

# print(x)

print(Score.archive)