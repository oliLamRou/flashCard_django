from django.db import models
from dictionary.models import Word
from django.contrib.auth.models import User

# Create your models here.
class Score(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='scores')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scores')
    fail = models.IntegerField(default=0)
    success = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    last_try = models.DateField(auto_now=True)
    archive = models.BooleanField(default=False)

    def __str__(self):
        foreignKey = f'User: {self.user.username} / word_id: {self.word.id}\n'
        score = f'Fail: {self.fail} / Success: {self.success} / Score: {self.score}\n'
        data = f'Last Try {self.last_try} / Is Archived: {self.archive}\n'
        return foreignKey + score + data