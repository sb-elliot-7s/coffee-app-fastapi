from fastapi import FastAPI
from account.routes import account_router
from account.profile_routes import profile_routers
from coffee.routes import coffee_router
from orders.routes import order_router
from kafka_producer import producer

app = FastAPI(title='Coffee app')


@app.on_event('startup')
async def startup_app():
    await producer.start()


@app.on_event('shutdown')
async def shutdown_app():
    await producer.stop()


app.include_router(account_router)
app.include_router(profile_routers)
app.include_router(coffee_router)
app.include_router(order_router)
