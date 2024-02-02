from django import forms
from .models import ImageSubmission

class ImageSubmissionForm(forms.ModelForm):
    class Meta:
        model = ImageSubmission
        fields = ['image', 'description']