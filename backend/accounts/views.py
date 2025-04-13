from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from accounts.forms import RegisterForm, PreferenceForm
from accounts.models import Preference

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    else:
        form = RegisterForm()
        
    return render(request, 'register.html', {'form': form})

def create_preference(request):
    pass

def preference_view(request):
    user_preferences = Preference.objects.filter(user=request.user).first()
    if user_preferences:
        if request.method == 'POST':
            form = PreferenceForm(request.POST, instance=user_preferences)
            if form.is_valid():
                form.save()
                return redirect('home')

        else:
            form = PreferenceForm(instance=user_preferences)

        return render(request, 'preference.html', {'form': form})
    else:
        if request.method == 'POST':
            form = PreferenceForm(request.POST)
            if form.is_valid():
                pref = form.save(commit=False)
                pref.user = request.user
                pref.save()
                return redirect('home')

        else:
            form = PreferenceForm()

        return render(request, 'preference.html', {'form': form})