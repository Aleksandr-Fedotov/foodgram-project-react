from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Тэг',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет',
        validators=[
            validators.RegexValidator(
                regex="#[A-Fa-f0-9]{6}",
                message='Укажите значение в HEX формате!',
                code='invalid_color'
            ),
        ]
    )
    slug = models.SlugField(
        verbose_name='Slug',
        max_length=200,
        unique=True
    )


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        ordering = ['-pk']
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'
            )
        ]


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipe_images/')
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        related_name='recipes'
    )
    tags = models.ManyToManyField(Tag, related_name='recipes')
    cooking_time = models.PositiveSmallIntegerField(
        validators=(validators.MinValueValidator(1),),
    )

    class Meta:
        ordering = ['-pk']


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        validators=(validators.MinValueValidator(1),),
    )

    class Meta:
        ordering = ['-pk']
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'recipe')
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
    )

    class Meta:
        ordering = ['-pk']
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe')
            )
        ]


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart'
    )

    class Meta:
        ordering = ['-pk']
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe')
            )
        ]
