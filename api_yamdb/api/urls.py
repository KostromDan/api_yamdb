from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import UserViewSet, register, token, CategoryViewset, GenreViewset#, TitleViewset

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='user')
router_v1.register('genres', GenreViewset)
router_v1.register('categories', CategoryViewset)
#router_v1.register('titles', TitleViewset)

urlpatterns = [
    path('v1/auth/token/', token,
         name='token_obtain_pair'),
    path('v1/auth/signup/', register,
         name='token_verify'),
    path('v1/', include(router_v1.urls)),