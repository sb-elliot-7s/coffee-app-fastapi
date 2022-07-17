from fastapi import status, responses
from .schemas import OrderCoffee, Order

response_data = {
    'detail_order': {
        'path': '/{order_id}',
        'status_code': status.HTTP_200_OK,
        'response_model': Order,
        'response_model_by_alias': False
    },
    'orders': {
        'path': '/',
        'status_code': status.HTTP_200_OK,
        'response_model': list[Order],
        'response_model_by_alias': False
    },
    'add_to_cart': {
        'path': '/{coffee_id}',
        'status_code': status.HTTP_201_CREATED,
        'response_model': OrderCoffee,
        'response_model_by_alias': False
    },
    'remove_from_cart': {
        'path': '/{order_coffee_id}',
        'response_model': OrderCoffee,
        'response_model_by_alias': False
    },
}


def coffee_order_completely_removed_response(order_coffee_id: str):
    return responses.JSONResponse(
        content={'detail': f'Coffee Order {order_coffee_id} completely removed'}
    )
