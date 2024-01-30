from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from .models import UserProfile

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


# 30/01/2024 - Modified this view. Severely. Should create a UserProfile instance AND create a User instance. Still haven't tested anything. Likely to blow up.

def registration_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save User
            user = form.save()

            # Create UserProfile instance
            UserProfile.objects.create(
                user=user,
                profile_image=request.POST.get('profile_image', ''),  # Update with the actual field names
                short_description=request.POST.get('short_description', ''),
                social_links=request.POST.get('social_links', ''),
                creation_date =request.POST.get('creation_date'),
            )
            # Log the user in (Optional)
            login(request, user)

            return redirect('main')  # Replace 'main' with your actual redirect URL
    else:
        form = UserCreationForm()

    return render(request, 'PhotoApp/registration.html', {'form': form})




# Come back to this to see how it works exactly, okay?
'''
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
'''