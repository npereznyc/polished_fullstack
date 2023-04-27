from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy
from .forms import LoginForm, RegisterForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

# class MyPasswordResetView(PasswordResetView):
#     template_name = 'accounts/password_reset_form.html'
#     email_template_name = 'password_reset_email.html'
#     subject_template_name = 'password_reset_subject.txt'
#     success_url = reverse_lazy('password_reset_done')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    # email_template_name = 'accounts/password_reset_email.html'
    # subject_template_name = 'accounts/templates/password_reset_subject'
    # THESE WILL NEED TO BE COMMENTED BACK IN BUT AT THE MOMENT THEY ARE INTERFEREING WITH THE REDIRECT...MAYBE THEY NEED TO COME AFTER THE SUCCESS_URL?
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('login')

# class MyPasswordResetConfirmView(PasswordResetConfirmView):
#     template_name = 'password_reset_confirm.html'
#     success_url = reverse_lazy('password_reset_complete')

# class MyPasswordChangeView(PasswordChangeView):
#     template_name = 'password_change_form.html'
#     success_url = reverse_lazy('password_change_done')