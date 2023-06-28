from bson import ObjectId

from schemas.base import UserBase


class UserOut(UserBase):
    _id: str
    first_name: str
    last_name: str
