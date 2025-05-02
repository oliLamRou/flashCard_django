from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.db.models import Prefetch

from dictionary.models import Word
from dictionary.serializers import WordSerializer

from learn.models import Score

from accounts.models import Preference
from accounts.serializers import PreferenceSerializer

@api_view(['POST', 'PATCH'])
def create(request):
    preference = Preference.objects.filter(user=request.user).first()
    if request.method == 'POST':
        word_instance = Word.objects.filter(
            user=request.user,
            **{f"{preference.languageA}": request.data[preference.languageA]},
            **{f"{preference.languageB}": request.data[preference.languageB]},
            ).first()
        
        if word_instance:
            return Response(status=422) #already exists

        serialized_word = WordSerializer(data=request.data, partial=True)
        if serialized_word.is_valid():
            serialized_word.save(user=request.user)
            return Response(serialized_word.data, status=201)
        else:
            return Response(serialized_word.errors, status=400)
        
    elif request.method == 'PATCH':
        data = request.data
        
        word_id = data.get('id')
        word_A = data.get(preference.languageA)
        word_B = data.get(preference.languageB)
        update_fields = {
            preference.languageA: word_A,
            preference.languageB: word_B,
            'description': data.get('description'),
            'word_class': data.get('word_class'),
        }        
        if not word_id or not word_A or not word_B:
            return Response(status=405)
        
        word_instance = Word.objects.filter(user=request.user, id=word_id)
        if word_instance:
            word_instance.update(**update_fields)
            return Response(status=201)
        else:
            return Response(status=405)
    else:
        return Response(status=405)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def get_word_classes(request):
    word_classes = {wc[0]: wc[1] for wc in Word.WORD_CLASS.choices}
    return Response({'word_classes': word_classes})

@api_view(['GET'])
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
        .order_by(*[lang_a])
    ) 

    words_serialized = WordSerializer(words, many=True)
    preference_serialized = PreferenceSerializer(preference, many=True)
    return Response({
        'words': words_serialized.data, 
        'preference': preference_serialized.data[0],
        })

@api_view(['POST'])
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
