from users.models import User
from recipes.models import Tag, Recipe, Ingredient, RecipeIngredient, RecipeTag
from rest_framework import permissions, serializers
from rest_framework.validators import UniqueValidator
from rest_framework.generics import get_object_or_404
import base64
from django.core.files.base import ContentFile

# ВЫПОЛНЕНО!
class UserSerializer(serializers.ModelSerializer):
    # role = serializers.StringRelatedField(read_only=True)
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        # допилить!
        return False


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Выберите другой логин.'
            )
        return value


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('email', 'password')


class AdminUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )



# ВЫПОЛНЕНО!
class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')

# ВЫПОЛНЕНО!
class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')

# ВЫПОЛНЕНО!
class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


"""class FollowSerializer(serializers.ModelSerializer):
    current_followers = serializers.SerializerNethodField()
    class Meta:
        model = Follow
        fields = ('..', 'current_followers')
    
    def get_current_followers(self, obj):
        return Follows.object.filter(id=id).count()"""


# ВЫПОЛНЕНО!
class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountSerializer(source='recipeingredient_set', many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    image = Base64ImageField(required=False)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'text', 'image', 'cooking_time', 'author', 'tags', 'ingredients')
    
    @staticmethod
    def get_ingredients(obj):
        ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return IngredientAmountSerializer(ingredients, many=True).data
    
    def validate(self, data):
        if 'tags' not in self.initial_data:
            raise serializers.ValidationError('Необходим минимум 1 тэг!')
        tags = self.initial_data.get('tags')
        tags_list = []
        for tag in tags:
            current_tag = get_object_or_404(Tag, id=tag['id'])
            if current_tag in tags_list:
                raise serializers.ValidationError('Тэги не должны повторяться!')
            tags_list.append(current_tag)
        data['tags'] = tags

        if 'ingredients' not in self.initial_data:
            raise serializers.ValidationError('Необходим минимум 1 ингредиент!')
        ingredients = self.initial_data.get('ingredients')
        ingredients_list = []
        for ingredient in ingredients:
            current_ingredient = get_object_or_404(Ingredient, id=ingredient['id'])
            if current_ingredient in ingredients_list:
                raise serializers.ValidationError('Ингредиенты не должны повторяться!')
            ingredients_list.append(current_ingredient)
        data['ingredients'] = ingredients

        return data

    def create(self, validated_data):
        #image = validated_data.pop('image')
        #ingredients_data = validated_data.pop('ingredients')
        #recipe = Recipe.objects.create(image=image, **validated_data)
        #tags_data = self.initial_data.get('tags')
        #recipe.tags.set(tags_data)
        #self.create_ingredients(ingredients_data, recipe)
        if 'tags' not in self.initial_data:
            recipe = Recipe.objects.create(**validated_data)
            return recipe
        tags_post = validated_data.pop('tags')
        ingredients_post = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags_post:
            current_tag, status = Tag.objects.get_or_create(**tag)
            RecipeTag.objects.create(recipe=recipe, tag=current_tag)

        for ingredient in ingredients_post:
            amount = ingredient.pop('amount')
            current_ingredient, status = Ingredient.objects.get_or_create(**ingredient)
            RecipeIngredient.objects.update_or_create(
                recipe=recipe,
                ingredient=current_ingredient,
                amount=amount
            )
        return recipe
