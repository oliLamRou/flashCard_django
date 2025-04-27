import json

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import Response

from accounts.models import Preference
from accounts.serializers import PreferenceSerializer

from commun.enums import LANGUAGE

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({'detail': 'CSRF cookie set'})

# API for login
def api_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = authenticate(username=data["username"], password=data["password"])
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Logged in"})
        else:
            return JsonResponse({"message": "Invalid credentials"}, status=401)

# API for logout
def api_logout(request):
    logout(request)
    return JsonResponse({"message": "Logged out"})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
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