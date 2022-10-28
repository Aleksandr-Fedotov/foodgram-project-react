from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.filters import AuthorAndTagFilter, IngredientSearchFilter
from api.pagination import SubscribeUserPagination
from api.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from api.serializers import (
    CropRecipeSerializer,
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
    FollowSerializer
)
from recipes.models import (
    Cart,
    Favorite,
    Ingredient,
    IngredientAmount,
    Recipe,
    Tag
)
from users.models import Follow

User = get_user_model()


class TagsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = SubscribeUserPagination
    filter_class = AuthorAndTagFilter
    permission_classes = [IsOwnerOrReadOnly]

    @staticmethod
    def __add_obj(model, user, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = CropRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def __delete_obj(model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.add_obj(Favorite, request.user, pk)
        return self.delete_obj(Favorite, request.user, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self.__add_obj(Cart, request.user, pk)
        return self.__delete_obj(Cart, request.user, pk)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = self.request.user
        ingredients = IngredientAmount.objects.filter(
            recipe__cart__user=user
        )

        shopping_cart = '\n'.join([
            f'{ingredient["amount"]} '
            for ingredient in ingredients])
        filename = 'shopping_list.txt'
        response = HttpResponse(shopping_cart, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
        # ing = ingredients.aggregate(Sum('amount'))
        # return get_ingredients_for_shopping(ingredients)


class SubscribeUserViewSet(UserViewSet):
    pagination_class = SubscribeUserPagination

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        follow = Follow.objects.create(user=user, author=author)
        serializer = FollowSerializer(
            follow, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        follow = Follow.objects.filter(user=user, author=author)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
