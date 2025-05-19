from django.db import models
from django.contrib.auth.models import User

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
    
    def __str__(self):
        return f'ID: {self.id} User: {self.user} FR: {self.FR} KR: {self.KR} WC: {self.word_class} Created: {self.create_at}\n'