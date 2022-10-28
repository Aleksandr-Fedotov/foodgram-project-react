from django.http import HttpResponse


def get_ingredients_for_shopping(ingredients):
    """
    shopping_list = []
    for item in list:
        shopping_list.append(
            f'{item} - {list[item]["amount"]} '
            f'{list[item]["measurement_unit"]} \n'
        )
    response = HttpResponse(shopping_list, 'Content-Type: text/plain')
    response['Content-Disposition'] = (
        'attachment; filename="shopping_list.txt"'
    )
    """
    shopping_cart = '\n'.join([
        f'{ingredient["ingredient__name"]} - {ingredient["total_amount"]} '
        f'{ingredient["ingredient__measurement_unit"]}'
        for ingredient in ingredients])
    filename = 'shopping_list.txt'
    response = HttpResponse(shopping_cart, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
