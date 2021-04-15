import unittest
import datetime

from database_loader import DatabaseLoader
from models import DiscordUser, GameSession

MODELS = [DiscordUser, GameSession]

# use an in-memory SQLite for tests.
test_db = DatabaseLoader.get_database(name="troll_bot_test", user="troll_bot_test")


class PeeweeBaseTestClass(unittest.TestCase):

    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

        now = datetime.datetime.now()
        print("Date now is: {}".format(now))
        hour = datetime.timedelta(hours=1)
        date_1_hour_before = now - hour
        print("Date one hour before: {}".format(date_1_hour_before))
        two_weeks = datetime.timedelta(weeks=2)
        date_two_weeks_before = now - two_weeks
        print("Date 2 weeks before: {}".format(date_two_weeks_before))
        three_weeks = datetime.timedelta(weeks=3)
        date_three_weeks_before = now - three_weeks
        print("Date 3 weeks before: {}".format(date_three_weeks_before))

        self.new_user = DiscordUser.create(id=1,
                                           name="test_user")
        self.session1 = GameSession.create(discord_user=self.new_user,
                                           session_start_time=date_1_hour_before,
                                           session_stop_time=now,
                                           session_duration_minutes=30)

        self.session2 = GameSession.create(discord_user=self.new_user,
                                           session_start_time=date_1_hour_before,
                                           session_stop_time=now,
                                           session_duration_minutes=30)

        self.new_user2 = DiscordUser.create(id=3,
                                            name="test_user2")

        self.session3 = GameSession.create(discord_user=self.new_user2,
                                           session_start_time=date_1_hour_before,
                                           session_stop_time=now,
                                           session_duration_minutes=60)

        self.session4 = GameSession.create(discord_user=self.new_user2,
                                           session_start_time=date_1_hour_before,
                                           session_stop_time=now,
                                           session_duration_minutes=60)

        self.session4 = GameSession.create(discord_user=self.new_user2,
                                           session_start_time=date_three_weeks_before,
                                           session_stop_time=date_two_weeks_before,
                                           session_duration_minutes=60)

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)
        # Close connection to db.
        test_db.close()

