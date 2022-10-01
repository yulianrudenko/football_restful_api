from django.urls import path

from . import views


app_name = 'auth'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('email-verify/', views.VerifyEmailView.as_view(), name='email_verify'),

    # path('login/', views.login_user, name='login'),
    # path('logout/', views.logout_user, name='logout'),
]
