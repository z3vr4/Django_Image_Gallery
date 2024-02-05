from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import ImageSubmissionForm
from django.contrib.auth.views import LoginView
from .models import UserProfile, ImageSubmission

def main_view(request):
    image_submissions = ImageSubmission.objects.all()

    context = {
        'image_submissions': image_submissions,
    }
    return render(request, 'PhotoApp/main.html', context)

def afterupload_view(request):
    return render(request, 'PhotoApp/afterupload.html')

def profile_view(request):
    if request.user.is_authenticated:
        # User is logged in, redirect to their profile detail page
        return redirect('detail_profile', username=request.user.username)
    else:
        return render(request, 'PhotoApp/profile.html')
    
def upload_view(request):
    if request.method == 'POST':
        form = ImageSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            image_submission = form.save(commit=False)
            if request.user.is_authenticated:
                image_submission.user = request.user.userprofile
            image_submission.save()
            return redirect('afterupload_view')  # Redirect to your success view
    else:
        form = ImageSubmissionForm()

    return render(request, 'PhotoApp/upload.html', {'form': form})

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

# Image submission detail view

def image_submission_detail_view(request, submission_id):
    image_submission = get_object_or_404(ImageSubmission, id=submission_id)

    context = {
        'image_submission': image_submission,
    }

    return render(request, 'PhotoApp/submissiondetail.html', context)
