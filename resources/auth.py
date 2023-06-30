from fastapi import APIRouter

from managers.user import UserManager
from schemas.request import user as user_schema

router = APIRouter(tags=["Auth"])


@router.post("/register", status_code=201)
async def register(user_data: user_schema.UserRegisterIn):
    token = await UserManager.register(user_data.dict())

    return {'token': token}


@router.post("/login")
async def login(user_data: user_schema.UserLoginIn):
    token = await UserManager.login(user_data.dict())

    return {'token': token}
