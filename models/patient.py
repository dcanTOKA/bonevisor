from typing import Optional

from user import User


class Patient(User):
    gender: str
    age: Optional[int]
    bone_age: float
