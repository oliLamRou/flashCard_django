import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flashcard.settings")
django.setup()

import json
from django.contrib.auth import get_user_model
from dictionary.models import Word

User = get_user_model()

# Replace with your actual username or user ID
username = 'oli'  # or use user_id = 1
try:
    user = User.objects.get(username=username)
except User.DoesNotExist:
    print(f"User '{username}' not found.")
    exit()

# Load the JSON file
with open('dumpdata.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

words = []
for row in data:
    modelName = row.get('model')
    if modelName != 'dictionary.word':
        continue

    words.append(row)

new_entries = []
for word in words:
    modelName = word.get('model')
    if modelName != 'dictionary.word':
        continue

    fields = word.get('fields')
    french = fields.get('french')
    korean = fields.get('korean')
    if not french or not korean:
        print('Skipping')
        continue

    
    exists = Word.objects.filter(user=user, FR=french, KR=korean).exists()
    # print(Word.objects.filter(user=user, FR='pomme', KR='사과'))
    
    if not exists:
        new_entries.append((french, korean))
        Word.objects.create(FR=french, KR=korean, user=user)

# Show what would be added
print(f"\n🔍 Check Mode: {len(new_entries)} new word(s) would be added for user '{user.username}'.\n")
for i, (french, korean) in enumerate(new_entries, 1):
    print(f"{i}. French: '{french}' → Korean: '{korean}'")
