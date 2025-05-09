import random
import math

from django.db.models import Q, F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.views import Response

from dictionary.models import Word
from dictionary.serializers import WordSerializer
from accounts.models import Preference
from learn.models import Score

def get_some_querySet(querySet, perc=1):
    queryList = list(querySet)
    queryListLen = len(queryList)
    random.shuffle(queryList)
    amount = math.ceil(queryListLen * perc)
    return queryList[:amount]

@api_view(['GET'])
def guess(request):
    if request.method == 'GET':
        preference = Preference.objects.filter(user=request.user).first()
        lang_from = preference.languageA if preference.learnMode == 'NORMAL' else preference.languageB
        lang_to = preference.languageB if preference.learnMode == 'NORMAL' else preference.languageA

        newPerc = preference.learnNewWordsPerc
        userPerc = preference.learnUserWordsPerc
        favPerc = preference.learnFavoriteWordsPerc
        failPerc = preference.learnFailWordsPerc
        succPerc = preference.learnSuccessWordsPerc

        qs = Word.objects.all() #Start Query

        #Get only user language
        qs = qs.exclude(Q(**{f"{lang_from}__isnull": True}) | Q(**{f"{lang_from}": ''}))
        qs = qs.exclude(Q(**{f"{lang_to}__isnull": True}) | Q(**{f"{lang_to}": ''}))

        if (userPerc < 1):
            qs = qs.filter(user=request.user)

        qs_noScore = qs.filter(scores__isnull=True) #get no score
        noScore_list = get_some_querySet(qs_noScore, newPerc)

        qs_withScore = qs.filter(scores__isnull=False) #get with score
        words_good = qs_withScore.filter(scores__success__gt=F('scores__fail')) #with score + more fail
        words_bad = qs_withScore.filter(scores__success__lte=F('scores__fail')) #with score + more success

        success_list = get_some_querySet(words_good, succPerc)
        fail_list = get_some_querySet(words_bad, failPerc)

        #Combien and shuffle
        word_list = noScore_list + success_list + fail_list
        random.shuffle(word_list)
        rdn_word = word_list[-1]

        print(f'Guess New Word: {getattr(rdn_word, lang_from)}')
        words = qs.filter(
            Q(
                **{
                    f'{lang_from}': getattr(rdn_word, lang_from)
                }
            )
        )

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
        print("CREATE:", created)
        
        if data.get('score') == -1:
            score_entry.fail += 1
        elif data.get('score') == 1:
            score_entry.success += 1

        score_entry.save()

        return HttpResponse(status=200)

    return HttpResponse(status=200)