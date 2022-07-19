import pytest
from ..logic import CalculateRatingService
from conftest import get_test_rating_collection
from .conftest import l3_rating, l2_rating, l1_rating, c1_rating, c2_rating, \
    g1_rating


class TestCalculateRating:

    @pytest.mark.parametrize('coffee_id, rating', [
        (*l1_rating,), (*l2_rating,), (*l3_rating,),
        (*c1_rating,), (*c2_rating,), (*g1_rating,)
    ])
    @pytest.mark.asyncio
    async def test_create_ratings(
            self, second_client_with_jwt_token, coffee_id, rating):
        response = await second_client_with_jwt_token.post(
            url=f'/coffee/rate/{coffee_id}',
            json={'rating': rating}
        )
        assert response.json()['rating'] == rating
        assert response.json()['coffee_id'] == coffee_id

    @pytest.mark.asyncio
    async def get_ratings(self):
        rating_collection = await get_test_rating_collection()
        service = CalculateRatingService(rating_collection=rating_collection)
        ratings = await service.calculate_rating()
        return [rating async for rating in ratings]

    @pytest.mark.asyncio
    async def test_calculate_rating(
            self, get_l_updated_rating, get_c_updated_rating,
            get_g_updated_rating
    ):
        ratings = await self.get_ratings()
        assert len(ratings) == 3
        sort_ratings = sorted(ratings, key=lambda x: x['avg_rating'])
        coffee_id_62d284e33a38023deac32849 = sort_ratings[0]
        coffee_id_62d29e657b350eb014e23663 = sort_ratings[1]
        coffee_id_62d2ae1dd1d42fcb93a745e9 = sort_ratings[2]

        assert coffee_id_62d2ae1dd1d42fcb93a745e9['coffee_id'] \
               == '62d2ae1dd1d42fcb93a745e9'
        assert coffee_id_62d29e657b350eb014e23663['coffee_id'] \
               == '62d29e657b350eb014e23663'
        assert coffee_id_62d284e33a38023deac32849['coffee_id'] \
               == '62d284e33a38023deac32849'

        assert coffee_id_62d2ae1dd1d42fcb93a745e9['avg_rating'] == \
               get_g_updated_rating
        assert coffee_id_62d29e657b350eb014e23663['avg_rating'] == \
               get_c_updated_rating
        assert coffee_id_62d284e33a38023deac32849['avg_rating'] == \
               get_l_updated_rating
