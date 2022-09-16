from django.db import models
from django.core.validators import MinValueValidator
from users.models import User
from colorfield.fields import ColorField


# ВЫПОЛНЕНО!
class Tag(models.Model):
    name = models.CharField(verbose_name='Тег', max_length=32, unique=True)
    color = ColorField(verbose_name='HEX-код цвета', default='#FF0000', unique=True)
    slug = models.SlugField(verbose_name='Идентификатор тега', unique=True)

    def __str__(self):
        return self.name

# ВЫПОЛНЕНО!
class Ingredient(models.Model):
    name = models.CharField(verbose_name='Ингредиент', max_length=100)
    measurement_unit = models.CharField(verbose_name='Единица измерения', max_length=100)

    def __str__(self):
        return self.name

# ВЫПОЛНЕНО!
class Recipe(models.Model):
    name = models.CharField(verbose_name='Название рецепта', max_length=200)
    text = models.TextField(verbose_name='Приготовление')
    image = models.ImageField(verbose_name='Изображение', upload_to='recipes/images/')
    public_date = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        default=30,
        validators=[MinValueValidator(1)]
    )
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
    )

    class Meta:
        ordering = ['-public_date',]

    def __str__(self):
        return self.name

# ВЫПОЛНЕНО!
class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'tag'),
                name='unique_recipes_tag'
            ),
        ]

# ВЫПОЛНЕНО!
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    amount = models.FloatField(
        validators=[MinValueValidator(0.1)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_recipes_ingredient'
            ),
        ]

    def __str__(self):
        return '{self.amount}'
