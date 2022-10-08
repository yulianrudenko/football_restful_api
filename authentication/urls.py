from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views


app_name = 'auth'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/email-verify/', views.VerifyEmailView.as_view(), name='email-verify'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('password-reset-request/', views.RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', views.TokenCheckPasswordResetView.as_view(), name='confirm-password-reset'),
    path('password-reset-perform/', views.PerformPasswordResetSerializer.as_view(), name='perform-password-reset'),
]
