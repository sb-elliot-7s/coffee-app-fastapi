from mongo_function import MongoFunctionMixin


class CalculateRatingService:

    def __init__(self, rating_collection):
        self.__rating_collection = rating_collection
        self.__mixin = MongoFunctionMixin()

    async def calculate_rating(self, skip: int = 0):
        pipeline = [
            self.__mixin.group_by(
                id_expression='$coffee_id',
                avg_rating={f'$avg': '$rating'}
            ),
            self.__mixin.project(avg_rating=1, coffee_id='$_id', _id=0),
            self.__mixin.skip(value=skip)
        ]
        return self.__rating_collection.aggregate(pipeline=pipeline)
