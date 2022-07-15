import pytest
from collections import namedtuple


class TestAuth:
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
    LESS_THAN_5_CHARACTERS_IN_PASSWORD = [
        {
            'loc': [
                'body', 'password'
            ],
            'msg': 'ensure this value has at least 5 characters',
            'type': 'value_error.any_str.min_length',
            'ctx': {'limit_value': 5}
        }
    ]
    User = namedtuple(
        typename='User',
        field_names=[
            'username',
            'password',
            'phone',
            'date_birth',
            'is_superuser'
        ]
    )

    first_user = User(
        username='first',
        password='12345',
        phone=12345,
        date_birth=None,
        is_superuser=False
    )
    second_user = User(
        username='admin',
        password='hello',
        phone=None,
        date_birth='1990-03-03 00:00',
        is_superuser=True
    )

    @pytest.mark.parametrize(
        'username, password, phone, date_birth, is_superuser, status',
        [(*first_user, 201), (*second_user, 201)]
    )
    @pytest.mark.asyncio
    async def test_signup(
            self, username, password, phone, date_birth, is_superuser, status,
            client_without_jwt
    ):
        response = await client_without_jwt.post(
            url='/account/registration',
            json={
                'username': username,
                'password': password,
                'phone': phone,
                'date_birth': date_birth,
                'is_superuser': is_superuser
            }
        )
        assert response.status_code == status
        assert response.json()['username'] == username
        assert response.json()['phone'] == phone
        assert response.json()['is_superuser'] == is_superuser
        assert 'password' not in response.json()

    @pytest.mark.parametrize('username, password, status, detail', [
        ('first', '12345', 400, 'User with this username exists'),
        ('new_username', '123', 422, LESS_THAN_5_CHARACTERS_IN_PASSWORD),
    ])
    @pytest.mark.asyncio
    async def test_failure_signup(
            self, client_without_jwt, username, password, status, detail
    ):
        response = await client_without_jwt.post(
            url='/account/registration',
            json={
                'username': username,
                'password': password
            }
        )
        assert response.status_code == status
        assert response.json()['detail'] == detail

    @pytest.mark.parametrize('username, password', [
        (first_user.username, first_user.password),
        (second_user.username, second_user.password)
    ])
    @pytest.mark.asyncio
    async def test_login(self, client_without_jwt, username, password):
        response = await client_without_jwt.post(
            url='/account/login',
            data={
                'username': username,
                'password': password
            },
            headers=self.HEADERS
        )
        assert response.status_code == 200
        assert 'access_token' in response.json()
        token: str = response.json()['access_token']
        assert len(token.split('.')) == 3

    @pytest.mark.parametrize('username, password, status, detail', [
        ('wrong_username', '123456', 400, 'Incorrect username or password'),
        ('first', 'wrong_password', 400, 'Incorrect username or password'),
    ])
    @pytest.mark.asyncio
    async def test_failure_login(
            self, client_without_jwt, username, password, status, detail
    ):
        response = await client_without_jwt.post(
            url='/account/login',
            data={'username': username, 'password': password},
            headers=self.HEADERS
        )
        assert response.status_code == status
        assert response.json()['detail'] == detail
