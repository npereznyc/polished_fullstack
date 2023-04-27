from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import LoginView, RegisterView, ResetPasswordView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password-reset/', ResetPasswordView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
         path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]