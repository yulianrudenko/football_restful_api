from django.urls import path
from django.views.generic import RedirectView
from django.urls import reverse_lazy

from . import views

app_name = 'api'

urlpatterns = [
    path('clubs/', views.ClubListView.as_view(), name='club-list'),
    path('clubs/<int:club_id>/', views.ClubDetailView.as_view(), name='club-detail'),

    path('players/', views.PlayerListView.as_view(), name='player-list'),
    path('players/<int:player_id>/', views.PlayerDetailView.as_view(), name='player-detail'),

    path('', RedirectView.as_view(url=reverse_lazy('api:player-list'))),
]
