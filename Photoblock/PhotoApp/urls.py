from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView, LoginView # logout view is built in view, same as Login

urlpatterns = [
    path('', main_view, name='main'),
    path('profile/', profile_view, name='profile'),
    path('upload/', upload_view, name='upload'),
    path('about', about_view, name='about_view'),
    path('login/', LoginView.as_view(template_name='registration/login.html',next_page='main'), name='login_view'),
    path('logout/', LogoutView.as_view(next_page='main'), name='logout_view'),
    path('registration/', registration_view, name='registration_view'),
    path('afterupload/', afterupload_view, name='afterupload_view'),
    path('profile/<str:username>/', detail_profile_view, name='detail_profile'),
    path('profile/<str:username>/edit', edit_profile_view, name='edit_profile'),
    path('profile/<str:username>/edit/delete', delete_profile_view, name='delete_profile'),
    path('profiledeleteconfirmation', delete_profile_confirmation, name="delete_profile_confirmation"),
    path('submission/<int:submission_id>/', image_submission_detail_view, name='image_submission_detail'),
    path('submission/<int:submission_id>/edit', edit_submission_view, name='edit_submission'),
    path('submission/<int:submission_id>/edit/delete', delete_submission_view, name='delete_submission'),
    path('submissiondeleteconfirmation', delete_submission_confirmation, name="delete_submission_confirmation")
]
