from typing import Optional
from fastapi import APIRouter, Depends
from .presenter import OrderPresenter
from .deps import get_account, get_service_data
from .responses_data import response_data

order_router = APIRouter(prefix='/orders', tags=['orders'])


@order_router.get(**response_data.get('detail_order'))
async def detail_order(
        order_id: str, service=Depends(get_service_data),
        account=Depends(get_account)
):
    return await OrderPresenter(**service) \
        .get_order(account=account, order_id=order_id)


@order_router.get(**response_data.get('orders'))
async def get_orders(
        skip: Optional[int] = 0, limit: Optional[int] = 10,
        is_ordered: Optional[bool] = False,
        service=Depends(get_service_data),
        account=Depends(get_account)
):
    return await OrderPresenter(**service).get_orders(
        account=account, skip=skip, limit=limit, is_ordered=is_ordered)


@order_router.post(**response_data.get('add_to_cart'))
async def add_to_cart(
        coffee_id: str,
        service=Depends(get_service_data),
        account=Depends(get_account)
):
    return await OrderPresenter(**service) \
        .add_to_cart(account=account, coffee_id=coffee_id)


@order_router.delete(**response_data.get('remove_from_cart'))
async def remove_from_cart(
        order_coffee_id: str,
        service=Depends(get_service_data),
        account=Depends(get_account)
):
    return await OrderPresenter(**service) \
        .remove_from_cart(order_coffee_id=order_coffee_id, account=account)
