from typing import Union


class MongoFunctionMixin:

    @staticmethod
    def set_document(**document):
        return {'$set': document}

    @staticmethod
    def filter(**queries): return queries

    @staticmethod
    def push_item(**field_value):
        return {'$push': field_value}

    @staticmethod
    def push_each_items(array_name: str, items: list):
        return {'$push': {array_name: {'$each': items}}}

    @staticmethod
    def inc(**kwargs):
        return {'$inc': kwargs}

    @staticmethod
    def match(query: dict):
        return {'$match': query}

    @staticmethod
    def add_fields(**field_with_expression):
        return {'$addFields': field_with_expression}

    @staticmethod
    def look_up(
            local_field: str,
            foreign_collection: str,
            foreign_field: str,
            _as: str
    ):
        return {
            '$lookup': {
                'from': foreign_collection,
                'localField': local_field,
                'foreignField': foreign_field,
                'as': _as
            }
        }

    @staticmethod
    def skip(value: int):
        return {'$skip': value}

    @staticmethod
    def limit(value: int):
        return {'$limit': value}

    @staticmethod
    def sort(**values):
        return {'$sort': values}

    @staticmethod
    def project(**expression):
        return {'$project': expression}

    @staticmethod
    def group_by(id_expression: Union[dict, str], **field_and_accumulator):
        return {
            '$group': {'_id': id_expression, **field_and_accumulator}
        }

    @staticmethod
    def round_value(value, decimal_place: int = 2):
        return {'$round': [value, decimal_place]}

    @staticmethod
    def map_aggregation(array_name: str, variable_name: str, expression: dict):
        return {
            '$map':
                {
                    'input': f'${array_name}',
                    'as': variable_name,
                    'in': expression
                }
        }

    @staticmethod
    def multiply(*expressions):
        return {'$multiply': [*expressions]}

    @staticmethod
    def sum_values(values: Union[str, list, dict]):
        return {'$sum': values}
