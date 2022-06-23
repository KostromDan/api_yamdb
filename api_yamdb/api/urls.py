from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import UserViewSet, register, token

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('v1/auth/token/', token,
         name='token_obtain_pair'),
    path('v1/auth/signup/', register,
         name='token_verify'),
    path('v1/', include(router_v1.urls)),
]
