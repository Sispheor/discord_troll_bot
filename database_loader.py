from peewee import MySQLDatabase

from settings_loader import SettingLoader


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DatabaseLoader(Singleton, object):

    @classmethod
    def get_database(cls, name="troll_bot"):
        settings = SettingLoader().settings
        return MySQLDatabase(database=name,
                             host=settings.database_host,
                             user=settings.database_user,
                             passwd=settings.database_password)
