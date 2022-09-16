from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from users.models import User


class Ingredients(models.Model):
    """Инградиенты."""
    name = models.TextField(
        verbose_name='Название инградиента',
        help_text='Добавьте инградиент')
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=20,
        help_text='Укажите единицу измерения')

    class Meta:
        verbose_name = 'Инградиенты'
        verbose_name_plural = 'Ингредиенты'
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    """Тэги."""
    name = models.TextField(
        verbose_name='Тэг',
        help_text='Добавьте тэг',
        unique=True)
    color = ColorField(
        default='#FF0000',
        verbose_name='Цвет тэга',
        help_text='Выберите цвет тэга'
    )
    slug = models.SlugField(
        verbose_name='Идентификатор тэга',
        help_text='Добавьте идентификатор тэга',
        unique=True,)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
                             
    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Рецепты."""
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='recipes',) 
    name = models.TextField(
        verbose_name='Название рецепта',
        help_text='Добавьте название')
    image = models.ImageField(
        verbose_name='Фото блюда',
        upload_to='recipes/media/',
    )
    description = models.TextField(
        verbose_name='Текст рецепта',
        help_text='Добавьте содержимое рецепта')
    ingredients = models.ManyToManyField(
        Ingredients,
        through='IngredientInRecipe',
        verbose_name='Инградиенты рецепта',
        help_text='Выбор инградиентов')
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэг',
        help_text='Тэг')
    time_cook = models.IntegerField(
        verbose_name='Время приготовления(в минутах)')
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date', ]

    def __str__(self):
        return self.name
        

class FavoriteRecipe(models.Model):
    """Рецепты в избранном."""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='favorite',
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Рецепт')

    class Meta:
        verbose_name_plural = 'Избранное'
        constraints = (
            UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_favorites',
            ),
        )

    def __str__(self):
        return f'{self.user} {self.recipe}'


class Cart(models.Model):
    """Покупки."""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='users_cart',
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart_recipes',
        verbose_name='Рецепт')

    class Meta:
        ordering = ['-id', ]
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = (
            UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_cart',
            ),
        )

    def __str__(self):
        return f'{self.recipe} {self.user}'


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient',
        verbose_name='Рецепт')
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe',
        verbose_name='Ингредиент')
    amount = models.IntegerField(
        validators=(MinValueValidator(1,
            message='Укажите количество больше нуля!',),),
        verbose_name='Количество',
        help_text='Введите количество ингредиента')

    class Meta:
        verbose_name_plural = 'Инградиенты в рецептах'
        constraints = (
            UniqueConstraint(
                fields=('recipe', 
                        'ingredient',),
                name='unique_ingredient_in_recipe',
            ),
        )

    def __str__(self):
        return f'{self.recipe}: {self.ingredient} – {self.amount}'
