from peewee import MySQLDatabase
from playhouse.pool import PooledMySQLDatabase

from settings_loader import SettingLoader


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DatabaseLoader(object):

    @classmethod
    def get_database(cls, name="troll_bot"):
        settings = SettingLoader().settings
        return PooledMySQLDatabase(
            database=name,
            max_connections=10,
            stale_timeout=300,
            user=settings.database_user,
            passwd=settings.database_password)

