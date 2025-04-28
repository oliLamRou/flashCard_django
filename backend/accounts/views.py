from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import Response

from django.contrib.auth.models import User

from accounts.models import Preference
from accounts.serializers import PreferenceSerializer
from accounts.models import Preference

from commun.enums import LANGUAGE

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        data = request.data
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return Response(status=422)
        
        if User.objects.filter(username=username).exists():
            return Response(status=422)
        
        new_user = User.objects.create_user(username=username, password=password)
        if new_user:
            print("New User Created", new_user.username)
            Preference.objects.create(user=new_user)
            return Response(status=201)
        
    return Response(status=500)

@api_view(['GET', 'POST'])
def preferences(request):
    if request.method == 'GET':
        modes = {mode[0]: mode[1] for mode in Preference.LEARN_MODE.choices}
        languages = {lang[0]: lang[1] for lang in LANGUAGE.choices}

        preferences = Preference.objects.filter(user=request.user)
        if not preferences:
            return Response({})

        serialized_preferences = PreferenceSerializer(preferences, many=True)
        return Response({
            'preferences': serialized_preferences.data[0],
            'modes': modes,
            'languages': languages
        })
    elif request.method == 'POST':
        preferences_instance, _ = Preference.objects.get_or_create(user=request.user)
        serialized_preferences = PreferenceSerializer(preferences_instance, data=request.data)
        
        if serialized_preferences.is_valid():
            serialized_preferences.save()
            return Response(200)
        
        else:
            return Response(500)