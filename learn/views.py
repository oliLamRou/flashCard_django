from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

from dictionary.models import Word
from learn.models import Score

def guess(request):
    word = Word.objects.order_by("?").first() #this is bad
    print(f'Guess New Word: {word.french}')

    return render(request, "guess.html", {"word": word})

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