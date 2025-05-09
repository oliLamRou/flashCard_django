from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Word(models.Model):    
    class WORD_CLASS(models.TextChoices):
        UNDEFINE = 'undef', 'undefine',
        NOUN = 'n', 'noun',
        VERB = 'v', 'verb',
        ADJECTIVE = 'adj', 'adjective',
        PRONOUN = 'pron', 'pronon',
        ADVERB = 'adv', 'adverb',
        ENDING = 'suff', 'ending',
        PARTICULE = 'part', 'particule',
        DETERMINER = 'det', 'determiner',
        INTERJECTION = 'int', 'interjection',
        NUMERAL = 'num', 'numeral',

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='words')
    FR = models.CharField(max_length=100, blank=True)
    KR = models.CharField(max_length=100, blank=True)
    EN = models.CharField(max_length=100, blank=True)
    description = models.TextField(default='', blank=True)
    word_class = models.CharField(max_length=20, choices=WORD_CLASS, default=WORD_CLASS.UNDEFINE)
    create_at = models.DateField(auto_now_add=True)

    def get_score_for(self, user):
        return self.score.filter(user=user).first()
    
    def __str__(self):
        # return super().__str__()
        return f'User: {self.user}\nFR: {self.FR}\nKR: {self.KR}\nEN: {self.EN}\nDescription: {self.description}\nWC: {self.word_class}\nCreated: {self.create_at}\n'

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