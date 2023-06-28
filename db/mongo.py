from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient

from db.settings import DBSettings


@lru_cache()
def get_database():
    settings_instance = DBSettings()
    client = AsyncIOMotorClient(settings_instance.mongo_connection_string)
    database = settings_instance.mongo_database_name

    return client[database]
