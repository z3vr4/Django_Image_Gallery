from django.shortcuts import render, redirect, get_object_or_404, get_or_create
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import ImageSubmissionForm, UserProfileForm, CommentForm
from django.contrib.auth.views import LoginView
from .models import *
from django.contrib.auth.decorators import login_required

# MAIN GRID OF STUFF
def main_view(request):
    image_submissions = ImageSubmission.objects.all()

    context = {
        'image_submissions': image_submissions,
    }
    return render(request, 'PhotoApp/main.html', context)


# PROFILE VIEW (for navbar "profile" button) (redirects if logged in)
def profile_view(request):
    if request.user.is_authenticated:
        # User is logged in, redirect to their profile detail page
        return redirect('detail_profile', username=request.user.username)
    else:
        return render(request, 'PhotoApp/profile.html')

# UPLOAD STUFF VIEW
def upload_view(request):
    if request.method == 'POST':
        form = ImageSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            image_submission = form.save(commit=False)
            if request.user.is_authenticated:
                image_submission.user = request.user.userprofile
            image_submission.save()


# This part might need future debugging
            tags_str = form.cleaned_data.get('tags', '')
            tags = [tag.strip().lower() for tag in tags_str.split(',') if tag.strip()]
            for tag_name in tags:
                # Normalize the tag name (remove spaces)
                backend_tag_name = tag_name.replace(' ', '').lower()

                # Create or retrieve the ImageTag instance
                tag, created = ImageTag.objects.get_or_create(
                    display_tag=tag_name,
                    backend_tag=backend_tag_name
                )

                # Add the tag to the image submission
                image_submission.tags.add(tag)
            return redirect('afterupload_view')  # Redirect to your success view
    else:
        form = ImageSubmissionForm()

    return render(request, 'PhotoApp/upload.html', {'form': form})

# FEEDBACK AFTER SUCCESFUL UPLOAD.
def afterupload_view(request):
    return render(request, 'PhotoApp/afterupload.html')

# ABOUT PAGE VIEW
def about_view(request):
    return render(request, 'PhotoApp/about.html')

# REGISTRATION VIEW
def registration_view(request):
    form = UserCreationForm(request.POST)

    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # Create UserProfile instance
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            print("UserProfile Created:", profile)
            # Log the user in
            authenticated_user = authenticate(username=user.username, password=request.POST['password1'])
            if authenticated_user:
                login(request, authenticated_user)
                return redirect('main')

        else:
            print("Form Errors:", form.errors)
            form = UserCreationForm()

    return render(request, 'PhotoApp/registration.html', {'form': form})

# Profile and image submission detail view
def detail_profile_view(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'PhotoApp/profiledetail.html', context)

def image_submission_detail_view(request, submission_id):
    image_submission = get_object_or_404(ImageSubmission, id=submission_id)
    image_comments = Comment.objects.filter(image_submission=image_submission)

    # Initialize the form with or without request.POST data
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                comment = form.save(commit=False)
                comment.user = request.user.userprofile
                comment.image_submission = image_submission
                comment.save()
                # Redirect after successful comment submission to prevent form resubmission
                return redirect('image_submission_detail', submission_id=submission_id)
    else:
        form = CommentForm()

    context = {
        'image_submission': image_submission,
        'image_comments': image_comments,
        'form': form, 
    }

    return render(request, 'PhotoApp/submissiondetail.html', context)

# Profile and image submission edit view
@login_required
def edit_profile_view(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('detail_profile', username=username)  # Redirect to profile detail view
    else:
        profile_form = UserProfileForm(instance=user_profile)

    context = {
        'user_profile': user_profile,
        'profile_form': profile_form
    }

    return render(request, 'PhotoApp/editprofile.html', context)

@login_required
def edit_submission_view(request, submission_id):
    image_submission = get_object_or_404(ImageSubmission, id=submission_id)
    image_comments = Comment.objects.filter(image_submission=image_submission)

    if request.method == 'POST':
        image_form = ImageSubmissionForm(request.POST, request.FILES, instance=image_submission)
        if image_form.is_valid():
            image_form.save()
            return redirect('image_submission_detail', submission_id=submission_id)  # Redirect to image detail view
    else:
        image_form = ImageSubmissionForm(instance=image_submission)

    context = {
        'image_submission': image_submission,
        'image_comments': image_comments,
        'image_form': image_form,
    }

    return render(request, 'PhotoApp/editsubmission.html', context)

# Image submission and profile deletion views
@login_required
def delete_submission_view(request, submission_id):
    image_submission = get_object_or_404(ImageSubmission, id=submission_id)
    
    # Ensure that only the owner of the image submission can delete it
    if image_submission.user.user != request.user:
        # Redirect to a different view in the future that tells users they're accessing a view they're not authorized to access, or whatever.
        return redirect('main')
    
    if request.method == 'POST':
        image_submission.delete()
        return redirect('delete_submission_confirmation')  # Make this redirect to a deletion confirmation view.

    # Render the deletion confirmation (asking you to confirm) page template
    return render(request, 'PhotoApp/deletesubmission.html', {'image_submission': image_submission})

def delete_submission_confirmation(request):
    return render(request, 'PhotoApp/afterdeleteprofile.html')

@login_required
def delete_profile_view(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)

    if user_profile.user != request.user:
        return redirect('main')
    
    if request.method == "POST":
        user_profile.delete()
        user_profile.user.delete()
        return redirect('delete_profile_confirmation')
    
    context = {
        'user_profile' : user_profile
    }
    
    return render(request, 'PhotoApp/deleteprofile.html', context)

def delete_profile_confirmation(request):
    return render(request, 'PhotoApp/afterdeleteimage.html')
