from peewee import MySQLDatabase


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DatabaseLoader(Singleton, object):

    @classmethod
    def get_database(cls, name="troll_bot", user="troll_bot", passwd="troll_bot_p@ssw0rd"):
        return MySQLDatabase(database=name, user=user, passwd=passwd)
