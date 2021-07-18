import logging
import os

from peewee import MySQLDatabase, SqliteDatabase

from models import database_proxy
from settings_loader import SettingLoader

logger = logging.getLogger('discord_bot')


def get_database(name="troll_bot"):
    settings = SettingLoader().settings
    logger.info("Get database called")
    is_test_env = os.getenv('TESTING_ENV', False)

    if is_test_env:
        logger.info("Setup testing database")
        db = SqliteDatabase(':memory:')
    else:
        logger.info("Setup Mysql database")
        db = MySQLDatabase(database=name,
                           host=settings.database_host,
                           user=settings.database_user,
                           passwd=settings.database_password)
    database_proxy.initialize(db)
    return db
