from django.contrib import admin
from recipes.models import Recipe, Tag, Ingredient, RecipeIngredient, RecipeTag


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author",)
    search_fields = ("name", "author",)
    list_filter = ("author", "name", "tags",)


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color",)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit",)
    search_fields = ("name",)
    list_filter = ("name",)
    ordering = ("name",)


class RecipesIngredientsAdmin(admin.ModelAdmin):
    list_display = ("recipe", "ingredient", "amount",)


class RecipesTagsAdmin(admin.ModelAdmin):
    list_display = ("recipe", "tag",)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient, RecipesIngredientsAdmin)
admin.site.register(RecipeTag, RecipesTagsAdmin)
