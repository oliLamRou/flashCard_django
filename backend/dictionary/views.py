from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from dictionary.models import Word
from dictionary.forms import WordForm

from learn.models import Score

from accounts.models import Preference

@login_required
def create(request):
    if request.method == 'POST':
        form = WordForm(request.POST, user=request.user)
        if form.is_valid():
            word = form.save(commit=False)
            word.user = request.user
            word.save()
            return redirect('word-list')
    else:
        form = WordForm(user=request.user)
    
    return render(request, 'word_form.html', {'form': form})

@login_required
def update(request, pk):
    word = get_object_or_404(Word, pk=pk)
    if request.method == 'POST':
        form = WordForm(request.POST, instance=word, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('word-list')
    else:
        form = WordForm(instance=word, user=request.user)
    return render(request, 'word_form.html', {'form': form})

@login_required
def read(request):
    preference = Preference.objects.filter(user=request.user).first()

    words = (
        Word.objects
        .prefetch_related(
           Prefetch(
                'scores',
                queryset=Score.objects.filter(user=request.user),
                to_attr='user_scores'  # so you can access it easily
            )
        )
        .exclude(**{f"{preference.languageA}__isnull": True})
        .exclude(**{f"{preference.languageA}": ''})
        .exclude(**{f"{preference.languageB}__isnull": True})
        .exclude(**{f"{preference.languageB}": ''})
    )

    for word in words:
        print(word.FR, word.KR, word.EN)

    return render(request, 'word_list.html', {'words': words, 'preference': preference})

@login_required
def delete(request, pk):
    preference = Preference.objects.filter(user=request.user).first()
    word = get_object_or_404(Word, pk=pk)
    if request.method == 'POST':
        word.delete()
        return redirect('word-list')
    return render(request, 'word_confirm_delete.html', {'word': word, 'preference': preference})



