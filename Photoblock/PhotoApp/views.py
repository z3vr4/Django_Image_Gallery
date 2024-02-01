from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import ImageSubmissionForm
from django.contrib.auth.views import LoginView
from .models import UserProfile, ImageSubmission

# Create your views here.

def main_view(request):
    return render(request, 'PhotoApp/main.html') # do the html templates and functionalities later.

def after_upload(request):
    return render(request, 'PhotoApp/main.html') # do the html templates and functionalities later.

def profile_view(request):
    if request.user.is_authenticated:
        # User is logged in, redirect to their profile detail page
        return redirect('detail_profile', username=request.user.username)
    else:
        return render(request, 'PhotoApp/profile.html')

def upload_view(request, user):
    form = ImageSubmissionForm(request.POST, request.FILES)
    if request.method == 'POST':
        print("request confirmed to be POST")
        if form.is_valid():
            # Create ImageSubmission instance
            image_submission = form.save(commit=False)
            image_submission.user = user  # Assuming 'user' is the currently logged-in user
            image_submission.save()
            print("Image Submission Created:", image_submission)
            return redirect('afterupload')
    return render(request, 'PhotoApp/upload.html', {'form': form})


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
                profile_image=request.POST.get('profile_image', ''),
                short_description=request.POST.get('short_description', ''),
                social_links=request.POST.get('social_links', ''),
                creation_date =request.POST.get('creation_date'),
            )
            print("UserProfile Created:", user_profile)
            # Log the user in
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