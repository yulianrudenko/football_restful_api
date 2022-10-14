from django.urls import path, include
from django.contrib import admin

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="FootWorld API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.ourapp.com/policies/terms/",
      contact=openapi.Contact(email="contact@footworld.local"),
      license=openapi.License(name="Test License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('auth/', include('authentication.urls', namespace='auth')),
    path('social-auth/', include('social_auth.urls', namespace='social-auth')),

    path('api/', include('players.urls', namespace='api')),
    path('api/chats/', include('chats.urls', namespace='chats')),

    path('admin/', admin.site.urls),

    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
