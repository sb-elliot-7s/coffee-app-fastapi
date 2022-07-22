from .logic import RecommendCoffee
from coffee.deps import coffee_collection


async def compute(title: str):
    recommend_coffee_service = RecommendCoffee(
        coffee_collection=coffee_collection
    )
    await recommend_coffee_service.transform_data_to_df()
    return recommend_coffee_service.recommend_coffee(title=title)
