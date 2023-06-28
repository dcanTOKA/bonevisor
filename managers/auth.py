from datetime import datetime, timedelta
from typing import Optional

import jwt
from decouple import config
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request

from db.mongo import get_database

db = get_database()
collection = db['users']


class AuthManager:
    @staticmethod
    def encode_token(user_data) -> str:
        try:
            payload = {
                "sub": str(user_data["_id"]),
                "exp": datetime.utcnow() + timedelta(minutes=120)
            }
            return jwt.encode(payload, config("SECRET_KEY"), algorithm="HS256")
        except Exception as exception:
            raise exception


class CustomHTTPBearer(HTTPBearer):
    async def __call__(
            self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)

        try:
            payload = jwt.decode(res.credentials, config("SECRET_KEY"), algorithms=["HS256"])
            user_data = await collection.find_one({'_id': payload['sub']})

            request.state.user = user_data

            return user_data
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token is expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")


oauth2_scheme = CustomHTTPBearer()
