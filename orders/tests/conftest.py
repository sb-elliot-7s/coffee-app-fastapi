# from main import app
# from ..mixins import RepositoryMixin


# def get_test_orders_pipeline(
#         self, skip: int, limit: int, is_ordered: bool, account
# ):
#     return [
#         self.match({'is_ordered': is_ordered, 'account_id': account.id}),
#         self.add_fields(order_id={'$toString': '$_id'}),
#         self.look_up(
#             local_field='order_id',
#             foreign_collection='test_coffee_order_collection',
#             foreign_field='order_id',
#             _as='coffees_order'
#         ),
#         self.skip(skip),
#         self.limit(limit),
#         self.sort(created=-1)
#     ]
#
#
# app.dependency_overrides[
#     RepositoryMixin().get_orders_pipeline
# ] = get_test_orders_pipeline
