from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.urls import reverse_lazy


urlpatterns = [
    path('api/', include('players.urls', namespace='api')),
    path('auth/', include('authentication.urls', namespace='auth')),

    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url=reverse_lazy('api:player-list'))),
]
