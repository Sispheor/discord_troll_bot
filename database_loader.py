import logging
import os

from peewee import MySQLDatabase, SqliteDatabase

from models import database_proxy

logger = logging.getLogger('discord_bot')


def get_database(name="troll_bot"):
    logger.info("Get database called")
    is_test_env = os.getenv('TESTING_ENV', False)

    if is_test_env:
        logger.info("Setup testing database")
        db = SqliteDatabase(':memory:')
    else:
        logger.info("Setup Mysql database")
        db = MySQLDatabase(database=os.getenv('MYSQL_DATABASE', name),
                           host=os.getenv('MYSQL_HOST', "127.0.0.1"),
                           user=os.getenv('MYSQL_USER', "troll_bot"),
                           passwd=os.getenv('MYSQL_PASSWORD', "troll_bot_p@ssw0rd"))
    database_proxy.initialize(db)
    return db
