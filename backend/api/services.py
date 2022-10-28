from django.http import HttpResponse


def get_ingredients_for_shopping(ingredients):
    shopping_list = []
    for item in ingredients:
        shopping_list.append(
            f'{item} - {ingredients[item]["amount"]} '
            f'{ingredients[item]["measurement_unit"]} \n'
        )
    response = HttpResponse(shopping_list, 'Content-Type: text/plain')
    response['Content-Disposition'] = (
        'attachment; filename="shopping_list.txt"'
    )
    return response
