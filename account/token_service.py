from datetime import datetime, timedelta
from jose import jwt, JWTError
from .interfaces.token_service_interface import TokenServiceInterface
from fastapi import status, HTTPException


class TokenService(TokenServiceInterface):
    async def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token=token, key=self.secret_key, algorithms=self.algorithm)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Could not validate credentials'
            )

    async def encode_token(self, username: str) -> str:
        data = {
            'sub': username,
            'exp': datetime.utcnow() + timedelta(minutes=self.exp_time)
        }
        return jwt.encode(
            claims=data, key=self.secret_key, algorithm=self.algorithm
        )
