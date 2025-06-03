import os
import requests
from dotenv import load_dotenv

from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from accounts.models import Preference
from accounts.serializers import PreferenceSerializer
from accounts.models import Preference

from commun.enums import LANGUAGE

def send_telegram_message(message):
    load_dotenv()
    # SECRETS = dotenv_values(find_dotenv())
    BOT_TOKEN = os.getenv("TELEGRAM_SECRET_KEY")
    CHAT_ID = os.getenv("CHAT_ID")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)

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
            send_telegram_message(f'New User: {username}')
            Preference.objects.create(user=new_user)
            return Response(status=201)
        
    return Response(status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            if username not in ['userA', 'userC']:
                send_telegram_message(f'{username} logged in')

            credentials = RefreshToken.for_user(user)
            print(f"New login for user: {user}\n")
            return Response({
                "access": str(credentials.access_token),
                "refresh": str(credentials)
            }, status=200)
        else:
            send_telegram_message(f'{username} failed login')

        return Response({"error": "Invalid credentials"}, status=401)    

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_tokens(request):
    if request.method == 'POST':
        refresh_token = request.data.get('refresh', None)
        if refresh_token is None:
            return Response({"error": "No refresh token"}, status=401)
        
        serializer = TokenRefreshSerializer(data={"refresh": refresh_token})
        if serializer.is_valid():
            print(f"Refresh login for user: {request.user}\n")
            return Response(serializer.validated_data, status=201)
        else:
            return Response(status=401)
    
    return Response(status=405)

@api_view(['GET', 'POST'])
def preferences(request):
    if request.method == 'GET':
        modes = {mode[0]: mode[1] for mode in Preference.LEARN_MODE.choices}
        deck = {mode[0]: mode[1] for mode in Preference.LEARN_DECK.choices}
        languages = {lang[0]: lang[1] for lang in LANGUAGE.choices}

        preferences = Preference.objects.filter(user=request.user)
        if not preferences:
            return Response({})

        serialized_preferences = PreferenceSerializer(preferences, many=True)
        return Response({
            'preferences': serialized_preferences.data[0],
            'modes': modes,
            'languages': languages,
            'deck': deck,
        }, status=200)
    elif request.method == 'POST':
        preferences_instance, _ = Preference.objects.get_or_create(user=request.user)
        serialized_preferences = PreferenceSerializer(preferences_instance, data=request.data)
        
        if serialized_preferences.is_valid():
            serialized_preferences.save()
            return Response(status=201)
        else:
            return Response(status=400)
        
    Response(status=405)

@api_view(['GET'])
# date_joined, email, first_name, groups, id, is_active, is_staff, is_superuser, last_login, last_name, logentry, password, preferences, scores, user_permissions, username, words
def user_info(request):
    if request.method == 'GET':
        user = User.objects.filter(username=request.user).first()
        if user:
            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
            return Response(data, status=200)
        else:
            return Response(status=422)
        
    return Response(status=405)