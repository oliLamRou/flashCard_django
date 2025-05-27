import secrets
from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.db.models import Q, F, Prefetch, ExpressionWrapper, DurationField, FilteredRelation
from django.db.models.functions import Now, ExtractDay

from rest_framework.decorators import api_view
from rest_framework.views import Response

from dictionary.models import Word
from dictionary.serializers import WordSerializer
from dictionary.models import Word

from learn.models import Score
from accounts.models import Preference

def get_random_word(user, preference):
    qs = Word.objects.annotate(
        user_score_rel=FilteredRelation(
        'scores',
        condition=Q(scores__user=user)
        )
    )

    #Archive
    qs = qs.exclude(Q(user_score_rel__archive=True))

    #Languages
    exclude_languages = (
        Q(**{f"{preference.languageA}__isnull": True}) | 
        Q(**{f"{preference.languageA}": ''}) |
        Q(**{f"{preference.languageB}__isnull": True}) | 
        Q(**{f"{preference.languageB}": ''})
    )
    qs = qs.exclude(exclude_languages)

    #User Choice
    if preference.learnDeck == 'FAVORITE':
        #FIX HERE WHEN FAV EXISTS
        pass
    elif preference.learnDeck == 'USER':
        qs = qs.filter(user=user)
    else:
        print("All Words")

    #In Progress & Revision
    days_since_last_try = ExtractDay(Now() - F("user_score_rel__last_try"))
    delay_days = ((F("user_score_rel__score") - 2) * 7) * ExtractDay(timedelta(days=1))

    qs = qs.annotate(
        days_since_last_try=ExpressionWrapper(days_since_last_try, output_field=DurationField()),
        delay_days=ExpressionWrapper(delay_days, output_field=DurationField()),
    )

    qs = qs.filter(
        (Q(user_score_rel__score__isnull=True)) | 
        (~Q(days_since_last_try=0) & Q(user_score_rel__score__lt=3)) |
        (Q(days_since_last_try__gt=0) & Q(days_since_last_try__gte=F("delay_days"))) |
        (Q(user_score_rel__fail=0) & Q(user_score_rel__success=0))
    )

    count = qs.count()
    if count:
        return qs[secrets.randbelow(count)]

def get_words_data(user, preference, rnd_word):
    #Prep Data for Frontend
    prefetch_score = Prefetch(
        'scores',
        queryset=Score.objects.filter(user=user),
        to_attr='user_score'
        )
    
    #NOTE: This multiple choice is a mess!
    # lang_from = preference.languageA if preference.learnMode == 'NORMAL' else preference.languageB
    # lang_from_words = Q(**{f'{lang_from}': getattr(rnd_word, lang_from)})
    # return Word.objects.prefetch_related(prefetch_score).filter(lang_from_words)    
    return Word.objects.prefetch_related(prefetch_score).filter(id=rnd_word.id)

@api_view(['GET'])
def guess(request):
    if request.method == 'GET':
        user = request.user
        preference = Preference.objects.filter(user=user).first()

        rnd_word = get_random_word(user, preference)
        if not rnd_word:
            return Response(status=204)
        
        words = get_words_data(user, preference, rnd_word)
        serialized_words = WordSerializer(words, many=True)

        print("New Word:", rnd_word.id, rnd_word.KR)
        print('Annotation', rnd_word.days_since_last_try, rnd_word.delay_days)
        print("Data", words[0].id, words[0].KR, '\n', words[0].user_score)

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