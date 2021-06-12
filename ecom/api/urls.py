from django.urls import path, include
# from rest_framework_authtoken import views
from .views import home

from rest_framework.authtoken.views import obtain_auth_token
#The drf provide an endpoint for the users to request an authentication token using their username and password


urlpatterns = [
    path('', home, name='api.home'),
    path('category/', include('api.category.urls')),
    path('product/', include('api.product.urls')),
    path('user/', include('api.user.urls')),
    path('order/', include('api.order.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
