import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flashcard.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Preference
from dictionary.models import Word

user = User.objects.filter(username='userA').first()
print(user.preferences)