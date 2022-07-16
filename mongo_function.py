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
