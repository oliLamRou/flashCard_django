import os
import django
import pandas as pd

data = pd.read_csv('_bu/data/words.csv')
# for row in data.iterrows():
#     print(row)

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flashcard.settings")
django.setup()

# Now, you can import your models
from dictionary.models import Word

# objects = Word.objects.all()
# for obj in objects:
#     print(obj.french, obj.create_at)

# Add new data
for row in data.iterrows():
    r = row[1]
    new_entry = Word(
        french = r['french'], 
        korean = r['korean'],
        create_at = r['created']
        )
    new_entry.save()

# print("New entry added:", new_entry)

for obj in Word.objects.all():
    print(obj.create_at, obj.french)