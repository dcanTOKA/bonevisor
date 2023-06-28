from bson import ObjectId
from fastapi import HTTPException
from passlib.context import CryptContext

from db.mongo import get_database
from managers.auth import AuthManager

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = get_database()
collection = db['users']


class UserManager:
    @staticmethod
    async def register(user_data):
        user_data["password"] = pwd_context.hash(user_data["password"])

        user = await collection.find_one({"email": user_data["email"]})

        if user:
            raise HTTPException(400, "User with this email already exists")
        else:
            result = await collection.insert_one(user_data)
            id_ = result.inserted_id

            user_do = await collection.find_one({"_id": ObjectId(id_)})

            return AuthManager.encode_token(user_do)

    @staticmethod
    async def login(user_data):
        user_do = await collection.find_one({"email": user_data['email']})
        if not user_do:
            raise HTTPException(400, "Wrong email or password")
        elif not pwd_context.verify(user_data['password'], user_do['password']):
            raise HTTPException(400, "Wrong email or password")

        return AuthManager.encode_token(user_do)

    @staticmethod
    async def get_all_users():
        users = collection.find()
        return [user async for user in users]

    @staticmethod
    async def get_user_by_email(email):
        fetched_user = await collection.find_one({"email": email})
        return fetched_user
