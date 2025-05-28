import math
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404

from dictionary.models import Word
from dictionary.serializers import WordSerializer

from learn.models import Score

from accounts.models import Preference

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

            id = serialized_word.data.get('id')
            word = get_object_or_404(Word, id=id)
            Score.objects.get_or_create(word=word, user=request.user)

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
            return Response({"error": "User or ID doesn't match"}, status=409)
    else:
        return Response(status=405)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def get_word_classes(request):
    word_classes = {wc[0]: wc[1] for wc in Word.WORD_CLASS.choices}
    return Response({'word_classes': word_classes})

@api_view(['GET'])
def read(request):
    if request.method == 'GET':
        preference = Preference.objects.filter(user=request.user).first()

        qs = Word.objects.prefetch_related(
            Prefetch(
                'scores',
                queryset=Score.objects.filter(user=request.user),
                to_attr='user_score'
            )
        )

        exclude_languages = (
            Q(**{f"{preference.languageA}__isnull": True}) | 
            Q(**{f"{preference.languageA}": ''}) |
            Q(**{f"{preference.languageB}__isnull": True}) | 
            Q(**{f"{preference.languageB}": ''})
        )
        qs = qs.exclude(exclude_languages)

        #filter user
        if request.query_params.get('all') == 'false':
            qs = qs.filter(user=request.user)

        #Search by
        #Order by
        qs = qs.order_by(*[preference.languageA])
        
        current_page = int(request.query_params.get('page', 0))
        row_per_page = 15
        page_amount = math.ceil(qs.count() / row_per_page)

        first_elem = current_page * row_per_page
        last_elem = first_elem + row_per_page

        words_serialized = WordSerializer(qs[first_elem:last_elem], many=True)
        data = {
            'words': words_serialized.data, 
            'page_amount': page_amount, 
            'current_page': current_page    
        }
        
        return Response(data, status=200)
    
    return Response(status=405)

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
