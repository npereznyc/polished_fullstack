from django.contrib import admin
from django.urls import path, include
from accounts.views import LoginView, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
    # path('login/', LoginView.as_view(), name='login'),
    # path('register/', RegisterView.as_view(), name='register'),
    path("accounts/", include("accounts.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    

]
