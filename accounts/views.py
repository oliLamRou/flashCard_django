from django.shortcuts import render, redirect
from django.contrib.auth import login
from accounts.forms import RegisterForm, PreferenceForm

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

def preference_view(request):
    if request.method == 'POST':
        form = PreferenceForm(request.POST)
        print(request.POST)
        if form.is_valid():
            pref = form.save(commit=False)
            pref.user = request.user
            pref.save()
            return redirect('home')

    else:
        form = PreferenceForm()

    return render(request, 'preference.html', {'form': form})