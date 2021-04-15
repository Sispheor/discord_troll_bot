import datetime

from database_loader import DatabaseLoader
from models import DiscordUser, GameSession
from tests.peewee_base_test_class import PeeweeBaseTestClass

MODELS = [DiscordUser, GameSession]

# use an in-memory SQLite for tests.
test_db = DatabaseLoader.get_database(name="troll_bot_test")


class TestModels(PeeweeBaseTestClass):

    def setUp(self):
        super(TestModels, self).setUp()

    def tearDown(self):
        super(TestModels, self).tearDown()

    def test_get_all_session_since_date(self):
        now = datetime.datetime.now()
        hour = datetime.timedelta(hours=2)
        date_2_hour_before = now - hour
        all_session = self.new_user2 .get_all_session_since_date(date_2_hour_before)
        self.assertEqual(2, len(all_session))

        four_weeks = datetime.timedelta(weeks=4)
        date_four_weeks_before = now - four_weeks
        all_session = self.new_user2 .get_all_session_since_date(date_four_weeks_before)
        self.assertEqual(3, len(all_session))

    def test_get_total_played_minute_for_session_list(self):
        self.assertEqual(60,
                         self.new_user.get_total_played_minute_for_session_list([self.session1, self.session2]))


