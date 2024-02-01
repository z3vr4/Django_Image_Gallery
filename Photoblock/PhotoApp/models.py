from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    short_description = models.TextField(max_length=255)
    social_links = models.TextField(blank=True)

class ImageSubmission(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image_submissions/')
    creation_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image_submission = models.ForeignKey(ImageSubmission, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
