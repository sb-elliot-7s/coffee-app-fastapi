from fastapi import FastAPI
from account.routes import account_router
from account.profile_routes import profile_routers
from coffee.routes import coffee_router
from orders.routes import order_router

app = FastAPI(title='Coffee app')

app.include_router(account_router)
app.include_router(profile_routers)
app.include_router(coffee_router)
app.include_router(order_router)
