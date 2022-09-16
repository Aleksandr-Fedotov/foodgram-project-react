
from django.db.models import F
# from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.serializers import CustomUserSerializer

from .models import Cart, FavoriteRecipe, IngredientInRecipe, Ingredients, Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    """Тэги."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class CartListSerializer(serializers.ModelSerializer):
    """Покупки."""
    class Meta:
        model = Cart
        fields = '__all__'


class IngredientsSerializer(serializers.ModelSerializer):
    """Инградиенты."""
    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Выводим инградиенты в рецепте"""
    id = serializers.ReadOnlyField(source='ingredient.id')
    #name = serializers.ReadOnlyField(source='ingredient.name')
    #unit = serializers.ReadOnlyField(source='ingredient.unit')
    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class FullIngredientInRecipeSerializer(serializers.ModelSerializer):
    """Выводим инградиенты в рецепте и списке рецептов"""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')
    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'amount', 'measurement_unit')


class AddIngredientInRecipeSerializer(serializers.ModelSerializer):
    """Добавление ингредиентов."""
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredients.objects.all())
    amount = serializers.IntegerField()
    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')
        

class ShortRecipeSerializer(serializers.ModelSerializer):
    """Вывод рецепта(после обновления или создания)."""
    ingredients = serializers.SerializerMethodField()
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    image = Base64ImageField()
    
    class Meta:
        model = Recipe
        fields = ('id','ingredients','tags', 'image', 'name', 'description', 'time_cook') # убери айди

    @staticmethod
    def get_ingredients(obj):
        ingredients = IngredientInRecipe.objects.filter(recipe=obj)
        return IngredientInRecipeSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        """Наличие рецепта в избранном."""
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return FavoriteRecipe.objects.filter(
            recipe=obj,
            user=request.user).exists()

    def get_is_in_cart(self, obj):
        """Проверка на наличие рецепта в списке покупок."""
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Cart.objects.filter(recipe=obj,
                                   user=request.user).exists()


class RecipeImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'time_cook')

    def get_image(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)


class CreateUpdateRecipeSerializer(serializers.ModelSerializer):
    """Для создания рецепта и обновления."""
    ingredients = AddIngredientInRecipeSerializer(many=True)
    image = Base64ImageField(use_url=True, max_length=None)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    name = serializers.CharField(max_length=200)
    time_cook = serializers.IntegerField()
    author = CustomUserSerializer(read_only=True)

    class Meta:
        fields =  ('id', 'author', 'ingredients', 'tags', 'image', 
                   'name', 'description', 'time_cook')
        model = Recipe

    @staticmethod
    def get_ingredients(obj):
        ingredients = IngredientInRecipe.objects.filter(recipe=obj)
        return IngredientInRecipeSerializer(ingredients, many=True).data

    def validate_ingredients(self, ingredients):
        """Проверка ингредиентов."""
        if not ingredients:
            raise ValidationError(
                'Необходимо выбрать ингредиенты!'
            )
        for ingredient in ingredients:
            if int(ingredient['amount']) <= 0:
                raise ValidationError(
                    'Количество ингредиентов должно быть больше нуля!'
                )
        ids = [item['id'] for item in ingredients]
        if len(ids) != len(set(ids)):
            raise ValidationError(
                'Ингредиенты в рецепте должны быть уникальными!'
            )
        return ingredients
  
    @staticmethod
    def add_ingredients(ingredients, recipe):
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            amount = ingredient['amount']
            if IngredientInRecipe.objects.filter(
                    recipe=recipe, ingredient=ingredient_id).exists():
                amount += F('amount')
            IngredientInRecipe.objects.update_or_create(
                recipe=recipe, ingredient=ingredient_id,
                defaults={'amount': amount}
            )
    
    def create(self, validated_data):
        author = self.context.get('request').user ###########
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        #image = validated_data.pop('image') #############
        recipe = Recipe.objects.create(author=author,
                                       **validated_data)
        self.add_ingredients(ingredients_data, recipe)
        recipe.tags.set(tags_data)
        return recipe

    def update(self, recipe, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        IngredientInRecipe.objects.filter(recipe=recipe).delete()
        self.add_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        return super().update(recipe, validated_data)

    def to_representation(self, recipe):
        data = ShortRecipeSerializer(
            recipe,
            context={'request': self.context.get('request')}).data
        return data
    
"""
class FavoriteRecipeSerializer(serializers.ModelSerializer):
    # Recipe для Избранного.
    image = Base64ImageField()
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'time_cook')


class ListFavoriteRecipeSerializer(serializers.ModelSerializer):
    # Избранные  рецепты.
    class Meta:
        model = FavoriteRecipe
        fields = '__all__'"""


class FullRecipeSerializer(serializers.ModelSerializer):
    """Вывод одного рецепта и списка рецептов"""
    image=Base64ImageField()
    ingredients = serializers.SerializerMethodField()
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_cart = serializers.SerializerMethodField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited', 
                  'is_in_cart', 'name', 'image', 'description', 'time_cook')
        model = Recipe

    @staticmethod
    def get_ingredients(obj):
        ingredients = IngredientInRecipe.objects.filter(recipe=obj)
        return FullIngredientInRecipeSerializer(ingredients, many=True).data

    def get_user(self):
        return self.context['request'].user

    def get_is_favorited(self, obj):
        """Наличие рецепта в избранном."""
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return FavoriteRecipe.objects.filter(
            recipe=obj,
            user=request.user).exists()

    def get_is_in_cart(self, obj):
        """Проверка на наличие рецепта в списке покупок."""
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Cart.objects.filter(recipe=obj,
                                   user=request.user).exists()
