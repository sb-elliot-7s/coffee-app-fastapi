from collections import namedtuple

import pytest

Rating = namedtuple('Rating', ['coffee_id', 'rating'])
l1_rating = Rating('62d284e33a38023deac32849', 3)
l2_rating = Rating('62d284e33a38023deac32849', 2)
l3_rating = Rating('62d284e33a38023deac32849', 1)
c1_rating = Rating('62d29e657b350eb014e23663', 2)
c2_rating = Rating('62d29e657b350eb014e23663', 5)
g1_rating = Rating('62d2ae1dd1d42fcb93a745e9', 5)
UpdatedRating = namedtuple('UpdatedRating', ['updated_rating'])
l_updated_rating = UpdatedRating(updated_rating=2.0)
c_updated_rating = UpdatedRating(updated_rating=3.5)
g_updated_rating = UpdatedRating(updated_rating=5.0)


@pytest.fixture
def get_l_updated_rating():
    return l_updated_rating.updated_rating


@pytest.fixture
def get_c_updated_rating():
    return c_updated_rating.updated_rating


@pytest.fixture
def get_g_updated_rating():
    return g_updated_rating.updated_rating
