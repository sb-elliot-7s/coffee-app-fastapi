from fastapi import status
from .schemas import CoffeeSchema, RateSchema

response_data = {
    'all': {
        'path': '/',
        'status_code': status.HTTP_200_OK,
        'response_model': list[CoffeeSchema],
        'response_model_by_alias': False
    },
    'detail': {
        'path': '/{coffee_id}',
        'status_code': status.HTTP_200_OK,
        'response_model': CoffeeSchema,
        'response_model_by_alias': False
    },
    'delete': {
        'path': '/{coffee_id}',
        'status_code': status.HTTP_204_NO_CONTENT,
    },
    'patch': {
        'path': '/{coffee_id}',
        'status_code': status.HTTP_200_OK,
        'response_model': CoffeeSchema,
        'response_model_by_alias': False
    },
    'post': {
        'path': '/',
        'status_code': status.HTTP_201_CREATED,
        'response_model': CoffeeSchema,
        'response_model_by_alias': False
    },
    'rate_coffee': {
        'path': '/rate/{coffee_id}',
        'status_code': status.HTTP_201_CREATED,
        'response_model': RateSchema,
        'response_model_by_alias': False
    },
    'update_rate_coffee': {
        'path': '/rate/{rating_id}',
        'status_code': status.HTTP_200_OK,
        'response_model': RateSchema,
        'response_model_by_alias': False
    }
}
