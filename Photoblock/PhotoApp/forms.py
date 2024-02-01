from django import forms
from .models import ImageSubmission


# come back to this to really understand it.
class ImageSubmissionForm(forms.ModelForm):
    class Meta:
        model = ImageSubmission
        fields = ['user', 'image', 'date','description']