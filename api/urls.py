from django.urls import path, include
from rest_framework import routers
from . import views as api_views
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

routers = routers.DefaultRouter()
routers.register(r'books', api_views.BookViewSet)
routers.register(r'authors', api_views.AuthorViewSet)
routers.register(r'places', api_views.PlaceViewSet)
routers.register(r'customers', api_views.CustomerViewSet)
routers.register(r'rents', api_views.RentViewSet)
routers.register(r'users', api_views.UserViewSet)

urlpatterns = [
    path('', include(routers.urls)),
    path('api-token-auth/', obtain_auth_token),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc-ui/', SpectacularRedocView.as_view(url_name='schema'), name='redoc-ui'),
]
