import pytest
from passlib.context import CryptContext

from ..password_service import PasswordService


class TestPasswordService:

    @pytest.fixture
    def get_password_context(self):
        return PasswordService(
            context=CryptContext(schemes=['bcrypt'], deprecated='auto'))

    @pytest.mark.parametrize('password', ['123456', 'hello_world'])
    @pytest.mark.asyncio
    async def test_successfully_verify_passwords(
            self, password, get_password_context
    ):
        hashed_password = await get_password_context.hashed_password(
            plain_password=password
        )
        assert await get_password_context.verify_passwords(
            plain_password=password, hashed_password=hashed_password
        )
