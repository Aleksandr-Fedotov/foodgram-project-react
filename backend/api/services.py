from django.http import HttpResponse


def creation_list(ingredients):
    shopping_list = '\n'.join([
        f'{ingredient["ingredient__name"]} - {ingredient["total"]} '
        f'{ingredient["ingredient__measurement_unit"]}'
        for ingredient in ingredients])
    response = HttpResponse(shopping_list, 'Content-Type: text/plain')
    response['Content-Disposition'] = (
        'attachment; filename="shopping_list.txt"'
    )
    return response
