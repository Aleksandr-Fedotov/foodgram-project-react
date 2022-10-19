from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import IngredientsViewSet, RecipeViewSet, TagsViewSet


app_name = 'api'

router = DefaultRouter()
router.register('tags1', TagsViewSet)
router.register('ingredients1', IngredientsViewSet)
router.register('r1ecipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
