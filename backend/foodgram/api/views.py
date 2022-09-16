from django.shortcuts import render
from rest_framework import filters, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, APIView
from django_filters.rest_framework import DjangoFilterBackend

from users.models import User
from recipes.models import Tag, Recipe, Ingredient
from api.serializers import (UserSerializer, TagSerializer, RecipeSerializer, IngredientSerializer)



# ВЫПОЛНЕНО!
class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

"""    def get_serializer_class(self):
        if self.action == 'list':
            return TagSerializer
        return TagPostSerializer"""

# ВЫПОЛНЕНО!
class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)  # .lower()

# ВЫПОЛНЕНО!
class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()



""" 
    def get_queryset(self):
        # Получаем id котика из эндпоинта
        cat_id = self.kwargs.get("cat_id")
        # И отбираем только нужные комментарии
        new_queryset = Comment.objects.filter(cat=cat_id)
        return new_queryset
"""

""" 
    list(self, request) — для получения списка объектов из queryset;
    create(self, request) — для создания объекта в модели;
    retrieve(self, request, pk=None) — для получения определённого объекта из queryset;
    update(self, request, pk=None) — для перезаписи (полного обновления) определённого объекта из queryset;
    partial_update(self, request, pk=None) — для частичного обновления объекта из queryset;
    destroy(self, request, pk=None) — для удаления одного из объектов queryset.
"""