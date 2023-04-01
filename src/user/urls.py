from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import register_view, verify_view, resend_code_view, sign_in_view, email_forgot_view, forgot_password_view, \
    DeleteProfileView, UserDetailView, UserUpdateView

urlpatterns = [
    path('sign-up/', register_view, name='sign_up'),
    path('sign-in/', sign_in_view, name='sign_in'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('verify/', verify_view, name='verify'),
    path('resend-code/', resend_code_view, name='resend_code'),
    path('email-forgot/', email_forgot_view, name='email_forgot'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('profile/<slug:guid>/', login_required(UserDetailView.as_view()), name='profile'),
    path('delete-profile/<slug:guid>/', login_required(DeleteProfileView.as_view()), name='delete_profile'),
    path('update-profile/<slug:guid>/', login_required(UserUpdateView.as_view()), name='update_profile')
]
