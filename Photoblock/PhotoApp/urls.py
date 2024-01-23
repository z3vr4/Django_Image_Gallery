# myapp/urls.py
from django.urls import path
from .views import main_view, profile_view, upload_view, login_view, registration_view
from django.contrib.auth.views import LogoutView, LoginView # logout view is built in view

urlpatterns = [
    path('', main_view, name='main'),
    path('profile/', profile_view, name='profile'),
    path('upload/', upload_view, name='upload'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login_view'),
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('registration/', registration_view.as_view(), name='registration_view'),
]
