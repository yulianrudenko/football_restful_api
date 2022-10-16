from django.urls import path

from . import views

app_name = 'social-auth'

urlpatterns = [
    path('facebook/', views.FacebookSocialAuthView.as_view(), name='facebook'),
    path('google/', views.GoogleSocialAuthView.as_view(), name='google'),
]
