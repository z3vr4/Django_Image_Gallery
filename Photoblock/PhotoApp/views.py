from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView

# Create your views here.

def main_view(request):
    return render(request, 'PhotoApp/main.html') # do the html templates and functionalities later.

def profile_view(request):
    return render(request, 'PhotoApp/profile.html')

def upload_view(request):
    return render(request, 'PhotoApp/upload.html')


# Login will be handled by built-in django view, so I think this is now useless. I commented it out Lul

#def login_view(request):
#    return render(request, 'PhotoApp/login.html')


# Come back to this to see how it works exactly, okay?
def registration_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
    else:
        form = UserCreationForm()

    return render(request, 'PhotoApp/registration.html', {'form': form})