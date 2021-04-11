import unittest
from datetime import datetime

from peewee import SqliteDatabase

from database_loader import DatabaseLoader
from models import DiscordUser, GameSession
from tests.peewee_base_test_class import PeeweeBaseTestClass

MODELS = [DiscordUser, GameSession]

# use an in-memory SQLite for tests.
test_db = DatabaseLoader.get_database(name="troll-bot-test.db")


class TestModels(PeeweeBaseTestClass):

    def setUp(self):
        super(TestModels, self).setUp()

    def tearDown(self):
        super(TestModels, self).tearDown()

    def test_get_all_session_since_date(self):
        date_limit = datetime(2020, 11, 1, 21, 00, 00, 0)
        all_session = self.new_user .get_all_session_since_date(date_limit)
        self.assertEqual(2, len(all_session))

        date_limit = datetime(2021, 11, 1, 22, 00, 00, 0)
        all_session = self.new_user .get_all_session_since_date(date_limit)
        self.assertEqual(1, len(all_session))

    def test_get_total_played_minute_for_session_list(self):
        self.assertEqual(60,
                         self.new_user.get_total_played_minute_for_session_list([self.session1, self.session2]))


