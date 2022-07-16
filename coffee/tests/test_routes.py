import pytest
from .common import CommonDataForTests
from image_service.image_service import ImageService
from database import database


class TestCoffeeRoutes:
    common_data = CommonDataForTests()

    @pytest.mark.asyncio
    async def test_empty_coffee(self, client_without_jwt):
        response = await client_without_jwt.get(url='/coffee/')
        assert response.status_code == 200
        assert len(response.json()) == 0

    @pytest.mark.parametrize('title, description, price, list_of_images', [
        (*common_data.LATTE,),
        (*common_data.CAPPUCCINO,),
        (*common_data.ESPRESSO,)
    ])
    @pytest.mark.asyncio
    async def test_create_coffee(
            self, admin_client_with_jwt, save_images,
            title, description, price, list_of_images
    ):
        data = {
            'title': title, 'description': description, 'price': price
        }
        response = await admin_client_with_jwt \
            .post(url='/coffee/', data=data,
                  files=save_images if list_of_images else None)
        assert response.status_code == 201
        assert response.json()['title'] == title
        self.common_data.IDS.append(response.json()['id'])
        self.common_data.IMAGES_ID.extend(response.json().get('images'))

    @pytest.mark.parametrize('limit, skip', [(10, 0)])
    @pytest.mark.asyncio
    async def test_list_of_all_coffees(
            self, client_without_jwt, limit, skip
    ):
        response = await client_without_jwt.get(
            url='/coffee/', params={'limit': limit, 'skip': skip})
        assert response.status_code == 200
        assert len(response.json()) == 3

    @pytest.mark.parametrize('coffee_id, status', [
        (common_data.first_id, 200),
        (common_data.seconds_id, 200),
        (common_data.third_id, 200),
        (common_data.get_wrong_coffee_id, 404)
    ])
    @pytest.mark.asyncio
    async def test_detail_coffee(self, client_without_jwt, coffee_id, status):
        response = await client_without_jwt.get(url=f'/coffee/{coffee_id()}')
        assert response.status_code == status

    @pytest.mark.parametrize(
        'coffee_id, title, description, price, list_of_images, status', [
            (common_data.first_id, *common_data.first_coffe_update, 200),
            (common_data.third_id, *common_data.third_coffee_update, 200),
            (common_data.get_wrong_coffee_id,
             *common_data.first_coffe_update, 404)
        ])
    @pytest.mark.asyncio
    async def test_update_coffee(
            self, admin_client_with_jwt, save_images,
            title, coffee_id, description, price, list_of_images, status
    ):
        response = await admin_client_with_jwt.patch(
            url=f'/coffee/{coffee_id()}',
            data={
                'title': title, 'description': description, 'price': price
            },
            files=save_images if list_of_images else None,
        )
        assert response.status_code == status
        if response.json().get('title'):
            assert response.json().get('title') == title
            assert response.json()['description'] == description
            self.common_data.IMAGES_ID.extend(response.json().get('images'))
        else:
            assert response.json().get('detail') == \
                   f'Coffee {coffee_id()} not found not found'

    @pytest.mark.parametrize('rating, coffee_id', [
        (*common_data.first_rating, common_data.first_id),
        (*common_data.third_rating, common_data.third_id)
    ])
    @pytest.mark.asyncio
    async def test_rate_coffee(
            self, first_client_with_jwt_token, rating, coffee_id
    ):
        response = await first_client_with_jwt_token.post(
            url=f'/coffee/rate/{coffee_id()}', json={'rating': rating})
        assert response.status_code == 201
        assert response.json()['rating'] == rating
        self.common_data.RATINGS_ID.append(response.json()['id'])

    @pytest.mark.parametrize('old_rating, new_rating, rating_id', [
        (*common_data.first_rating, 5, common_data.first_rating_id),
        (*common_data.third_rating, 4, common_data.third_rating_id)
    ])
    @pytest.mark.asyncio
    async def test_change_rate(
            self, first_client_with_jwt_token, old_rating, new_rating, rating_id
    ):
        response = await first_client_with_jwt_token.patch(
            url=f'/coffee/rate/{rating_id()}', json={'rating': new_rating})
        assert response.status_code == 200
        assert response.json()['rating'] == new_rating
        assert response.json()['rating'] != old_rating

    @pytest.mark.parametrize('coffee_id, status, resp', [
        (common_data.first_id, 204, None),
        (common_data.get_wrong_coffee_id, 404,
         {'detail': f'Coffee {common_data.wrong_coffee_id} not found'})
    ])
    @pytest.mark.asyncio
    async def test_delete_coffee(
            self, admin_client_with_jwt, coffee_id, status, resp
    ):
        response = await admin_client_with_jwt.delete(
            url=f'/coffee/{coffee_id()}')
        assert response.status_code == status
        assert response.json() == resp

        new_response = await admin_client_with_jwt.get(url='/coffee/')
        assert len(new_response.json()) == 2

    @pytest.mark.asyncio
    async def test_delete_images(self):
        for image in set(self.common_data.IMAGES_ID):
            await ImageService(database=database).delete_image(image_id=image)
