from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
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


# 30/01/2024 - Modified this view. Severely. Should create a UserProfile instance AND create a User instance.
# 31/01/2024 - Tested it, blew up some times, fixed it.

def registration_view(request):
    form = UserCreationForm(request.POST)
    if request.method == 'POST':
        print("request confirmed to be POST")
        if form.is_valid():
            # Save User
            user = form.save()

            # Create UserProfile instance
            user_profile = UserProfile.objects.create(
                user=user,
                profile_image=request.POST.get('profile_image', ''),  # Update with the actual field names
                short_description=request.POST.get('short_description', ''),
                social_links=request.POST.get('social_links', ''),
                creation_date =request.POST.get('creation_date'),
            )
            print("UserProfile Created:", user_profile)
            # Log the user in (Optional)
            authenticated_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if authenticated_user:
                login(request, authenticated_user)
                return redirect('main')

    else:
        print("Form Errors:", form.errors)
        form = UserCreationForm()

    return render(request, 'PhotoApp/registration.html', {'form': form})

# User profile detail view

def detail_profile_view(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'PhotoApp/profiledetail.html', context)