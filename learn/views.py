import random
import math
from django.http import HttpResponse, JsonResponse
from django.db.models import F
from django.shortcuts import render, get_object_or_404

from dictionary.models import Word
from learn.models import Score

def get_some_querySet(querySet, perc=1):
    queryList = list(querySet)
    queryListLen = len(queryList)
    random.shuffle(queryList)
    amount = math.ceil(queryListLen * perc)
    return queryList[:amount]

def guess(request):
    WORDS_GOOD_PERC = 0.01
    WORDS_BAD_PERC = 0.05

    #New
    words_without_score = Word.objects.filter(score__isnull=True).order_by("?")
    
    #Score
    words_with_score = Word.objects.filter(score__isnull=False)
    words_good = words_with_score.filter(score__success__gt=F('score__fail'))
    words_bad = words_with_score.filter(score__success__lte=F('score__fail'))

    #Get all or some query
    words_without_score_list = get_some_querySet(words_without_score)
    words_good_list = get_some_querySet(words_good, WORDS_GOOD_PERC)
    words_bad_list = get_some_querySet(words_bad, WORDS_BAD_PERC)

    #Combien and shuffle
    word_list = words_without_score_list + words_good_list + words_bad_list
    random.shuffle(word_list)
    word = word_list[-1]

    print(f'Guess New Word: {word.french}')

    otherWord = Word.objects.filter(french=word.french) #.exclude(korean=word.korean)
    print(otherWord)

    return render(request, "guess.html", {"word": word, "otherWord": otherWord})

def score(request):
    if request.method == "POST":
        print(f'request: {request.POST}')
        answer = request.POST.get("answer")
        word_id = request.POST.get("wordID")

        word = get_object_or_404(Word, id=word_id)
        score_entry, created = Score.objects.get_or_create(word=word)
        
        if answer == 'bad':
            score_entry.fail += 1
        elif answer == 'good':
            score_entry.success += 1

        print(f'New Score for: {score_entry.word.french} fail: {score_entry.fail} success: {score_entry.success}')
        return HttpResponse(status=200)

    return HttpResponse(status=200)