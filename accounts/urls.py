from django.urls import path

from accounts.views import LoginView, RegisterView, MyPasswordResetView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password-reset/', MyPasswordResetView.as_view(), name='password-reset'),
]