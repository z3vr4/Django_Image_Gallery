from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def main_view(request):
    return render(request, 'PhotoApp/main.html') # do the html templates and functionalities later.

def profile_view(request):
    return render(request, 'PhotoApp/profile.html')

def upload_view(request):
    return render(request, 'PhotoApp/upload.html')

def login_view(request):
    return render(request, 'PhotoApp/login.html')