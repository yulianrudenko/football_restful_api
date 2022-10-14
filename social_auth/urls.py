from django.urls import path

from . import views

app_name = 'social-auth'

urlpatterns = [
    path('facebook/', views.FacebookSocialAuthView.as_view()),
]
