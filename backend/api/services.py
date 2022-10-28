from django.http import HttpResponse


def get_ingredients_for_shopping(ingredients):
    shopping_cart = '\n'.join([
        f'{ingredient["ingredient__name"]} - {ingredient["total_amount"]} '
        f'{ingredient["ingredient__measurement_unit"]}'
        for ingredient in ingredients])
    filename = 'shopping_list.txt'
    response = HttpResponse(shopping_cart, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
