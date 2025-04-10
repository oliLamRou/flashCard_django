from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from dictionary.models import Word
from dictionary.forms import WordForm

from learn.models import Score

@login_required
def create(request):
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            word = form.save(commit=False)
            word.user = request.user
            word.save()
            return redirect('word-list')
    else:
        form = WordForm()
    
    return render(request, 'word_form.html', {'form': form})

@login_required
def read(request):
    # words = Word.objects.all().order_by('french')
    words = Word.objects.prefetch_related(
        Prefetch(
            'scores',
            queryset=Score.objects.filter(user=request.user),
            to_attr='user_scores'  # so you can access it easily
        )
    )
    return render(request, 'word_list.html', {'words': words})

@login_required
def update(request, pk):
    word = get_object_or_404(Word, pk=pk)
    if request.method == 'POST':
        form = WordForm(request.POST, instance=word)
        if form.is_valid():
            form.save()
            return redirect('word-list')
    else:
        form = WordForm(instance=word)
    return render(request, 'word_form.html', {'form': form})

@login_required
def delete(request, pk):
    word = get_object_or_404(Word, pk=pk)
    if request.method == 'POST':
        word.delete()
        return redirect('word-list')
    return render(request, 'word_confirm_delete.html', {'word': word})



