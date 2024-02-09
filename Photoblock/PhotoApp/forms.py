from django import forms
from .models import ImageSubmission, UserProfile, Comment

class ImageSubmissionForm(forms.ModelForm):
    class Meta:
        model = ImageSubmission
        fields = ['image', 'description']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'short_description', 'social_links']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']