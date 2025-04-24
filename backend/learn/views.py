import random
import math

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from rest_framework.views import Response

from dictionary.models import Word
from dictionary.serializers import WordSerializer

from accounts.serializers import PreferenceSerializer


from django.http import HttpResponse
from django.db.models import F
from django.shortcuts import render, get_object_or_404

from learn.models import Score
from accounts.models import Preference

def get_some_querySet(querySet, perc=1):
    queryList = list(querySet)
    queryListLen = len(queryList)
    random.shuffle(queryList)
    amount = math.ceil(queryListLen * perc)
    return queryList[:amount]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def guess(request):
    if request.method == 'GET':
        WORDS_GOOD_PERC = 0.01
        WORDS_BAD_PERC = 0.05

        word = Word.objects.filter(user=request.user).order_by("?").first()
        serialized_word = WordSerializer(word)

        preference = Preference.objects.filter(user=request.user).first()
        serialized_preferences = PreferenceSerializer(preference)


        return Response({"word": serialized_word.data, 'preferences': serialized_preferences.data})
    
    return Response(status=402)
    # # lang_from = preference.languageA if preference.learnMode == preference.LEARN_MODE.normal else preference.languageB
    # # lang_to = preference.languageB if lang_from == preference.languageA else preference.languageA
    # lang_to = preference.languageB if preference.learnMode == 'NORMAL' else preference.languageA

    # #New
    # words_without_score = (
    #     Word.objects
    #     .filter(scores__isnull=True)
    #     # .filter(user=request.user) #Not sure yet.
    #     .exclude(**{f"{preference.languageA}__isnull": True})
    #     .exclude(**{f"{preference.languageA}": ''})
    #     .exclude(**{f"{preference.languageB}__isnull": True})
    #     .exclude(**{f"{preference.languageB}": ''})
    #     .order_by("?")
    # )
    
    # #Score
    # words_with_score = (
    #     Word.objects
    #     .filter(scores__isnull=False)
    #     .exclude(**{f"{preference.languageA}__isnull": True})
    #     .exclude(**{f"{preference.languageA}": ''})
    #     .exclude(**{f"{preference.languageB}__isnull": True})
    #     .exclude(**{f"{preference.languageB}": ''})
    # )
    # words_good = words_with_score.filter(scores__success__gt=F('scores__fail'))
    # words_bad = words_with_score.filter(scores__success__lte=F('scores__fail'))

    # #Get all or some query
    # words_without_score_list = get_some_querySet(words_without_score)
    # words_good_list = get_some_querySet(words_good, WORDS_GOOD_PERC)
    # words_bad_list = get_some_querySet(words_bad, WORDS_BAD_PERC)

    # #Combien and shuffle
    # word_list = words_without_score_list + words_good_list + words_bad_list
    # random.shuffle(word_list)
    # word = word_list[-1]

    # print(f'Guess New Word: {getattr(word, preference.languageA)}')

    # #This is like : filter(FR=word.FR)
    # otherWord = (
    #     Word.objects
    #     .filter(**{f'{lang_to}': getattr(word, lang_to)})
    #     .exclude(**{f"{preference.languageA}__isnull": True})
    #     .exclude(**{f"{preference.languageA}": ''})
    #     .exclude(**{f"{preference.languageB}__isnull": True})
    #     .exclude(**{f"{preference.languageB}": ''})        
    # )

    # return Response({"word": word, "otherWord": otherWord, "preference": preference})
    return Response({"word": serialized_word})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def score(request):
    if request.method == "POST":
        print(f'request: {request.data}')
        # answer = request.POST.get("answer")
        # word_id = request.POST.get("wordID")

        data = request.data
        if not data:
            return Response(status=404)
        
        word = get_object_or_404(Word, id=data.get('id'))
        if not word:
            return Response(status=404)
        
        score_entry, created = Score.objects.get_or_create(word=word, user=request.user)
        print("CREATE:", created)
        
        if data.get('score') == -1:
            score_entry.fail += 1
        elif data.get('score') == 1:
            score_entry.success += 1

        score_entry.save()

        # print(f'New Score for: {score_entry.word.french} fail: {score_entry.fail} success: {score_entry.success}')
        return HttpResponse(status=200)

    return HttpResponse(status=200)