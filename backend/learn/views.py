import random
import secrets
from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.db.models import Q, F, Prefetch, ExpressionWrapper, IntegerField, DurationField
from django.db.models.functions import Now

from rest_framework.decorators import api_view
from rest_framework.views import Response

from dictionary.models import Word
from dictionary.serializers import WordSerializer
from dictionary.models import Word

from learn.models import Score
from accounts.models import Preference


@api_view(['GET'])
def guess(request):
    if request.method == 'GET':
        user = request.user
        preference = Preference.objects.filter(user=user).first()

        #Score Prefetch
        prefetch_score = Prefetch(
            'scores',
            queryset=Score.objects.filter(user=user, archive=False),
            to_attr='user_scores'
            )
        qs = Word.objects.prefetch_related(prefetch_score)

        #Valid values in language
        exclude_languages = (
            Q(**{f"{preference.languageA}__isnull": True}) | 
            Q(**{f"{preference.languageA}": ''}) |
            Q(**{f"{preference.languageB}__isnull": True}) | 
            Q(**{f"{preference.languageB}": ''})
        )
        qs = qs.exclude(exclude_languages)

        #Archive
        qs = qs.filter(scores__archive=False)

        #User Choice
        if preference.learnDeck == 'FAVORITE':
            #FIX HERE WHEN FAV EXISTS
            pass
        elif preference.learnDeck == 'USER':
            qs = qs.filter(user=user)

        #Score or Date
        delay_days_expression = ExpressionWrapper((F("scores__score") - 2) * 7, output_field=IntegerField())
        days_since_last_try_expression = ExpressionWrapper(Now() - F("scores__last_try"), output_field=DurationField())
        qs = qs.annotate(
            delay_days=delay_days_expression,
            days_since_last_try=days_since_last_try_expression
        )
        
        delay_days_result = Q(delay_days__lt=1) | Q(days_since_last_try__gte=F("delay_days") * timedelta(days=1))
        qs = qs.filter(delay_days_result)#Aka score < 3 or waiting >= delay

        #Random and select
        queryList = list(qs)
        i = secrets.randbelow(len(queryList))
        random.shuffle(queryList)
        rnd_word = queryList[i]

        #Get all match
        lang_from = preference.languageA if preference.learnMode == 'NORMAL' else preference.languageB
        filter_lang_from = Q(**{f'{lang_from}': getattr(rnd_word, lang_from)})
        words = qs.filter(filter_lang_from).distinct('id')

        serialized_words = WordSerializer(words, many=True)
        return Response({"words": serialized_words.data}, status=200)        
    
    return Response(status=405)

@api_view(['POST'])
def score(request):
    if request.method == "POST":
        data = request.data
        if not data:
            return Response(status=404)
        
        word = get_object_or_404(Word, id=data.get('id'))
        if not word:
            return Response(status=404)
        
        score_entry, created = Score.objects.get_or_create(word=word, user=request.user)
        
        if data.get('score') == -1:
            score_entry.fail += 1
            score_entry.score = 0
        elif data.get('score') == 1:
            score_entry.success += 1
            score_entry.score += 1

        score_entry.save()

        return Response(status=200)

    return Response(status=405)

@api_view(['POST'])
def archive(request):
    if request.method == "POST":
        data = request.data
        if not data:
            return Response(status=404)

        word = get_object_or_404(Word, id=data.get('id'))
        if not word:
            return Response(status=404)
    
        score_entry, created = Score.objects.get_or_create(word=word, user=request.user)

        if data.get("archive") == True:
            score_entry.archive = True
        elif data.get("archive") == False:
            score_entry.archive = False
        else:
            return Response(status=400)
            
        score_entry.score = 0
        score_entry.save()
        return Response(status=200)   
    
    return Response(status=405)     