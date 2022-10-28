from django.http import HttpResponse


def get_ingredients_for_shopping(list):
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
    return response
