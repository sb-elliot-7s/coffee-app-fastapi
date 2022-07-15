from datetime import datetime, timedelta
import time

import pytest
from fastapi import HTTPException
from configs import get_configs


class TestTokenService:

    @pytest.mark.parametrize('username', ['test123', 'test321'])
    @pytest.mark.asyncio
    async def test_successfully_create_token(self, username, get_token_service):
        token = await get_token_service.encode_token(username=username)
        assert len(token.split('.')) == 3

    @pytest.mark.parametrize('username', ['hello', 'world'])
    @pytest.mark.asyncio
    async def test_decode_token(self, username, get_token_service):
        exp_time = get_configs().exp_time
        token = await get_token_service.encode_token(username=username)
        data = await get_token_service.decode_token(token=token)
        assert data.get('sub') == username
        assert data.get('sub') is not None
        current_datetime = datetime.fromtimestamp(time.time())

        current_plus_delta = (current_datetime + timedelta(minutes=exp_time)) \
            .strftime('%Y-%m-%d %H:%M')
        expected_datetime = datetime.fromtimestamp(data.get('exp')) \
            .strftime('%Y-%m-%d %H:%M')
        assert expected_datetime == current_plus_delta

    @pytest.mark.asyncio
    async def test_failure_decode_token(self, get_token_service):
        wrong_token = '6f0138010c645ed8ac24b0ac37846065.' \
                      '6f0138010c645ed8ac24b0ac37846065.' \
                      '6f0138010c645ed8ac24b0ac37846065'
        with pytest.raises(HTTPException):
            await get_token_service.decode_token(token=wrong_token)
