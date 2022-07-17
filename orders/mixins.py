from bson import ObjectId

from mongo_function import MongoFunctionMixin
from configs import get_configs


class AggPipelineMixin(MongoFunctionMixin):
    __foreign_collection = \
        'test_coffee_order_collection' if get_configs().test else 'order_coffee'

    def __add_total_amount_fields(self):
        return self.add_fields(
            total_amount={
                **self.round_value(
                    value=self.sum_values(
                        self.map_aggregation(
                            array_name='coffees_order',
                            variable_name='coffee',
                            expression=self.multiply(
                                '$$coffee.quantity', '$$coffee.price'
                            )
                        )
                    )
                )
            }
        )

    def __add__lookup(self):
        return self.look_up(
            local_field='order_id',
            foreign_collection=self.__foreign_collection,
            foreign_field='order_id',
            _as='coffees_order'
        )

    def get_orders_pipeline(
            self, skip: int, limit: int, is_ordered: bool, account):
        return [
            self.match({'is_ordered': is_ordered, 'account_id': account.id}),
            self.add_fields(order_id={'$toString': '$_id'}),
            self.__add__lookup(),
            self.__add_total_amount_fields(),
            self.skip(skip),
            self.limit(limit),
            self.sort(created=-1)
        ]

    def get_order_pipeline(self, order_id: str, account):
        return [
            self.match({'_id': ObjectId(order_id), 'account_id': account.id}),
            self.add_fields(order_id={'$toString': '$_id'}),
            self.__add__lookup(),
            self.__add_total_amount_fields()
        ]
