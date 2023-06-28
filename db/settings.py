import enum
from functools import lru_cache

from pydantic import BaseSettings, Field

from decouple import config


class ConfigDB(enum.Enum):
    DB_USER = config('DB_USER')
    DB_PASSWORD = config('DB_PASSWORD')
    DB_HOST = config('DB_HOST')
    DB_PORT = str(config('DB_PORT'))
    DB_NAME = config('DB_NAME')


if len(ConfigDB.DB_USER.value) + len(ConfigDB.DB_PASSWORD.value) != 0:
    CONNECTION_STRING = f"mongodb://{ConfigDB.DB_USER.value}:{ConfigDB.DB_PASSWORD.value}@{ConfigDB.DB_HOST.value}:{ConfigDB.DB_PORT.value}"
else:
    CONNECTION_STRING = f"mongodb://{ConfigDB.DB_HOST.value}:{ConfigDB.DB_PORT.value}"


class DBSettings(BaseSettings):
    # MongoDB Settings
    mongo_connection_string: str = Field(
        CONNECTION_STRING,
        title="MongoDB Movies Connection string",
        description="The connection string for the MongoDB database.",
    )
    mongo_database_name: str = Field(
        str(ConfigDB.DB_NAME.value),
        title="MongoDB Movies Database name",
        description="The database name for the MongoDB Movies database.",
    )


@lru_cache()
def settings_instance():
    """
    Settings instance to used as a Fast API dependency.
    """
    return DBSettings()
