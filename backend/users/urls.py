from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import SubscribeUserViewSet

app_name = 'users'

router = DefaultRouter()
router.register('users', SubscribeUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]