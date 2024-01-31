from django.urls import path
from .views import main_view, profile_view, upload_view, registration_view, detail_profile_view
from django.contrib.auth.views import LogoutView, LoginView # logout view is built in view, same as Login

urlpatterns = [
    path('', main_view, name='main'),
    path('profile/', profile_view, name='profile'),
    path('upload/', upload_view, name='upload'),
    path('login/', LoginView.as_view(template_name='registration/login.html',next_page='main'), name='login_view'),
    path('logout/', LogoutView.as_view(next_page='main'), name='logout_view'),
    path('registration/', registration_view, name='registration_view'),
    path('profile/<str:username>/', detail_profile_view, name='detail_profile'),
]
