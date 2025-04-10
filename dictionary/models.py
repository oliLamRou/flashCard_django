from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Word(models.Model):
    class WORD_CLASS(models.TextChoices):
        UNDF = 'UNDEFINE',
        NOUN = 'NOUN',
        VERB = 'VERB',
        ADJECTIVE = 'ADJ',
        PRONOUN = 'PRON',
        ADVERB = 'ADV',
        ENDING = 'END',
        PARTICULE = 'PART',
        DETERMINER = 'DET',
        INTERJECTION = 'INTJ',
        NUMERAL = 'NUM',

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='words')
    french = models.CharField(max_length=100)
    korean = models.CharField(max_length=100)
    description = models.TextField(default='')
    word_class = models.CharField(max_length=20, choices=WORD_CLASS, default=WORD_CLASS.UNDF)
    create_at = models.DateField(auto_now_add=True)

    def get_score_for(self, user):
        return self.score.filter(user=user).first()

'''
noun	명사	[myeong-sa]
verb	동사	[dong-sa]
adjective	형용사	[hyeong-yong-sa]
pronoun	대명사	[dae-myeong-sa]
adverb	부사	[bu-sa]
ending	어미	[eom-i]
particle	조사	[jo-sa]
determiner	관형사	[gwan-hyeong-sa]
interjection	감탄사	[gam-tan-sa]
numeral	수사	[su-sa]
'''