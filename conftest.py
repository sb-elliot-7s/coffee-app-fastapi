import asyncio

import pytest
from httpx import AsyncClient

from configs import get_configs
from account.token_service import TokenService
from main import app
import motor.motor_asyncio
from account.deps import get_account_collection
from coffee.deps import get_coffee_collection, get_rating_collection


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope='session')
def get_token_service():
    return TokenService(
        exp_time=get_configs().exp_time,
        algorithm=get_configs().algorithm,
        secret_key=get_configs().secret_key
    )


test_client = motor.motor_asyncio.AsyncIOMotorClient(
    get_configs().mongo_url
)


async def get_test_db():
    return test_client.test_database


async def get_test_account_collection():
    db = await get_test_db()
    return db.test_account_collection


async def get_test_coffee_collection():
    db = await get_test_db()
    return db.test_coffee_collection


async def get_test_rating_collection():
    db = await get_test_db()
    return db.test_rating_collection


@pytest.fixture(scope='session')
async def session():
    test_database = await get_test_db()
    yield
    test_client.drop_database(name_or_database='test_database')


@pytest.fixture(scope='session')
@pytest.mark.asyncio
async def client_without_jwt(session) -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        yield client


async def save_user(client, username: str, password: str):
    data = {'username': username, 'password': password}
    res = await client.post(url='/account/registration', json=data)
    return res.json()


@pytest.fixture(scope='module')
async def first_user(client_without_jwt):
    return await save_user(
        client_without_jwt, username='elliot', password='1234567890'
    )


async def retrieve_access_token(token_service: TokenService, username: str):
    return await token_service.encode_token(username=username)


@pytest.fixture(scope='module')
@pytest.mark.asyncio
async def first_client_with_jwt_token(
        get_token_service: TokenService, first_user) -> AsyncClient:
    token = await retrieve_access_token(token_service=get_token_service,
                                        username=first_user['username'])
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        client.headers.update({'Authorization': f'Bearer {token}'})
        yield client


@pytest.fixture(scope='module')
async def admin_user(client_without_jwt):
    response = await client_without_jwt.post(
        url='/account/registration',
        json={
            'username': 'admin_user',
            'password': '123456',
            'is_superuser': True
        }
    )
    return response.json()


@pytest.fixture(scope='module')
@pytest.mark.asyncio
async def admin_client_with_jwt(
        get_token_service: TokenService, admin_user) -> AsyncClient:
    token = await retrieve_access_token(
        get_token_service, username=admin_user['username']
    )
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        client.headers.update({'Authorization': f'Bearer {token}'})
        yield client


app.dependency_overrides[get_account_collection] = get_test_account_collection
app.dependency_overrides[get_coffee_collection] = get_test_coffee_collection
app.dependency_overrides[get_rating_collection] = get_test_rating_collection
