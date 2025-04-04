from django.shortcuts import render, redirect, get_object_or_404
from dictionary.models import Word
from dictionary.forms import WordForm

def create(request):
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('word-list')
    else:
        form = WordForm()
    
    return render(request, 'word_form.html', {'form': form})

def read(request):
    words = Word.objects.all()
    return render(request, 'word_list.html', {'words': words})

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

def delete(request, pk):
    word = get_object_or_404(Word, pk=pk)
    if request.method == 'POST':
        word.delete()
        return redirect('word-list')
    return render(request, 'word_confirm_delete.html', {'word': word})



