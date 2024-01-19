# myapp/urls.py
from django.urls import path
from .views import main_view, profile_view, upload_view, login_view

urlpatterns = [
    path('', main_view, name='main'),
    path('profile/', profile_view, name='profile'),
    path('upload/', upload_view, name='upload'),
    path('login/', login_view, name='login'),
]

# we have no templates done, remember to make em later