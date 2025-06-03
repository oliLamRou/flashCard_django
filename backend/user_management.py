import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flashcard.settings')
django.setup()

from django.contrib.auth.models import User

users = User.objects.all()

for user in users:
    print(user)

# print("\n-------")
# selectedUser = User.objects.filter(username='antoine').first()
# if selectedUser:
#     print("Selected User:", selectedUser.username)
#     print(selectedUser.user_score)
    # selectedUser.delete()