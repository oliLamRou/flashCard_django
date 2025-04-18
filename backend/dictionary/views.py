from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from dictionary.models import Word
from dictionary.forms import WordForm
from dictionary.serializers import WordSerializer

from learn.models import Score

from accounts.models import Preference
from accounts.serializers import PreferenceSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    if request.method == 'POST':
        preference = Preference.objects.filter(user=request.user).first()
        word_instance = Word.objects.filter(
                user=request.user,
                **{f"{preference.languageA}": request.data[preference.languageA]},
                **{f"{preference.languageB}": request.data[preference.languageB]},
            ).first()
        
        if word_instance:
            serialized_word = WordSerializer(word_instance, data=request.data, partial=True)
        else:
            serialized_word = WordSerializer(data=request.data, partial=True)

        if serialized_word.is_valid():
            serialized_word.save(user=request.user)
            return Response(serialized_word.data, status=201 if not word_instance else 200)
        else:
            return Response(serialized_word.errors, status=400)

    return Response(status=405)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_word_classes(request):
    word_classes = {wc[0]: wc[1] for wc in Word.WORD_CLASS.choices}
    return Response({'word_classes': word_classes})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read(request):
    preference = Preference.objects.filter(user=request.user)
    lang_a = preference.first().languageA
    lang_b = preference.first().languageB

    words = (
        Word.objects
        .prefetch_related(
           Prefetch(
                'scores',
                queryset=Score.objects.filter(user=request.user),
                to_attr='user_scores'
            )
        )
        .exclude(**{f"{lang_a}__isnull": True})
        .exclude(**{f"{lang_a}": ''})
        .exclude(**{f"{lang_b}__isnull": True})
        .exclude(**{f"{lang_b}": ''})
    ) 

    words_serialized = WordSerializer(words, many=True)
    preference_serialized = PreferenceSerializer(preference, many=True)
    return Response({
        'words': words_serialized.data, 
        'preference': preference_serialized.data[0],
        })

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete(request):
    if request.method == 'POST':
        word_id = request.data.get('id')

        if not word_id:
            return Response({'error': 'Missing word ID'}, status=400)
        
        word_instance = Word.objects.filter(pk=word_id, user=request.user)
        if word_instance:
            word_instance.delete()
            return Response(status=204)
        else:
            return Response({'error': 'Word not found'}, status=404)

    return Response(status=405)
