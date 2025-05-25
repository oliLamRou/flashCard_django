import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flashcard.settings')
django.setup()

import random
import secrets
from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.db.models import Q, F, Prefetch, ExpressionWrapper, IntegerField, DurationField, CharField, FilteredRelation
from django.db.models.functions import Now, ExtractDay, ExtractWeek

from rest_framework.decorators import api_view
from rest_framework.views import Response

from dictionary.models import Word
from dictionary.serializers import WordSerializer
from dictionary.models import Word

from learn.models import Score
from accounts.models import Preference
from django.contrib.auth.models import User
from accounts.models import Preference
from dictionary.models import Word
from learn.models import Score

word = Word.objects.filter(id=44).first()
user = User.objects.filter(username='userQ').first()

score = Score.objects.filter(user=user)

print(score)