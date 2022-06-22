from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewset, GenreViewset#, TitleViewset

router = DefaultRouter()
router.register('genres', GenreViewset)
router.register('categories', CategoryViewset)
#router.register('titles', TitleViewset)

urlpatterns = [
    path('v1/', include(router.urls)),
]
