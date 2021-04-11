import unittest
from datetime import datetime

from database_loader import DatabaseLoader
from models import DiscordUser, GameSession

MODELS = [DiscordUser, GameSession]

# use an in-memory SQLite for tests.
test_db = DatabaseLoader.get_database(name="troll-bot-test.db")


class PeeweeBaseTestClass(unittest.TestCase):

    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

        self.new_user = DiscordUser.create(id=1,
                                           name="test_user")
        date_start = datetime(2021, 11, 1, 21, 00, 00, 0)
        date_end = datetime(2021, 11, 1, 21, 30, 00, 0)
        self.session1 = GameSession.create(discord_user=self.new_user,
                                           session_start_time=date_start,
                                           session_stop_time=date_end,
                                           session_duration_minutes=30)

        date_start = datetime(2021, 11, 1, 22, 00, 00, 0)
        date_end = datetime(2021, 11, 1, 22, 30, 00, 0)
        self.session2 = GameSession.create(discord_user=self.new_user,
                                           session_start_time=date_start,
                                           session_stop_time=date_end,
                                           session_duration_minutes=30)

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)
        # Close connection to db.
        test_db.close()

