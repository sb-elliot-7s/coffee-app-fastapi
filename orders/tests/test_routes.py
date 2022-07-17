import pytest
from .common import CommonDataForTests


class TestOrderRoutes:
    common_data = CommonDataForTests()

    @pytest.mark.parametrize('title, desc, price', [
        ('t1', 'd1', 1.34),
        ('t2', 'd2', 2.28),
        ('t3', 'd3', 3.7)
    ])
    @pytest.mark.asyncio
    async def test_create_three_coffees(
            self, admin_client_with_jwt, title, desc, price
    ):
        response = await admin_client_with_jwt.post(
            url='/coffee/',
            data={
                'title': title,
                'description': desc,
                'price': price
            }
        )
        self.common_data.COFFEE_IDS.append(response.json()['id'])

    @pytest.mark.asyncio
    async def test_empty_get_orders(self, second_client_with_jwt_token):
        response = await second_client_with_jwt_token.get(
            url='/orders/', params={
                'skip': 0, 'limit': 10, 'is_ordered': False
            }
        )
        assert len(response.json()) == 0
        assert response.status_code == 200

    @pytest.mark.parametrize('coffee_id, qnt', [
        (common_data.get_first_coffee_id, 1),
        (common_data.get_second_coffee_id, 1),
        (common_data.get_third_coffee_id, 1),
        (common_data.get_first_coffee_id, 2),
        (common_data.get_first_coffee_id, 3),
        (common_data.get_third_coffee_id, 2),
    ])
    @pytest.mark.asyncio
    async def test_add_to_cart(
            self, second_client_with_jwt_token, coffee_id, qnt
    ):
        response = await second_client_with_jwt_token \
            .post(url=f'/orders/{coffee_id()}')
        assert response.status_code == 201
        assert response.json()['coffee_id'] == coffee_id()
        assert response.json()['quantity'] == qnt
        self.common_data.COFFEE_ORDER_IDS.append(response.json()['id'])

    @pytest.mark.asyncio
    async def test_get_orders(self, second_client_with_jwt_token):
        response = await second_client_with_jwt_token.get(
            url='/orders/', params={'skip': 0, 'limit': 5, 'is_ordered': False}
        )
        assert len(response.json()) == 1
        assert response.status_code == 200
        assert len(response.json()[0]['coffees_order']) == 3
        self.common_data.ORDER_IDS.append(response.json()[0]['id'])

    @pytest.mark.parametrize('order_id', [common_data.get_order_id])
    @pytest.mark.asyncio
    async def test_get_order(self, second_client_with_jwt_token, order_id):
        response = await second_client_with_jwt_token.get(
            url=f'/orders/{order_id()}'
        )
        assert response.status_code == 200
        assert response.json()['id'] == order_id()
        assert not response.json()['is_ordered']

    @pytest.mark.parametrize('coffee_order_id, status, key, value', [
        (common_data.get_first_coffee_order_id, 200, 'quantity', 2),
        (common_data.get_second_coffee_order_id, 200, 'detail',
         'Coffee Order {} completely removed'),
        (common_data.get_third_coffee_order_id, 200, 'quantity', 1),
        (common_data.get_wrong_coffee_order, 404, 'detail',
         'Order Coffee 62d3f37d28cb8a5fc5dffe42 not found')
    ])
    @pytest.mark.asyncio
    async def test_remove_from_cart(
            self, second_client_with_jwt_token, coffee_order_id, status, key,
            value
    ):
        response = await second_client_with_jwt_token.delete(
            url=f'/orders/{coffee_order_id()}'
        )
        assert response.status_code == status
        if 'quantity' not in response.json():
            assert response.json()[key] == value.format(coffee_order_id())
        else:
            assert response.json()[key] == value
