import datetime
from unittest.mock import MagicMock

import models
from game_session_manager import GameSessionManager
from models import DiscordUser
from tests.peewee_base_test_class import PeeweeBaseTestClass


class TestGameSessionManager(PeeweeBaseTestClass):

    def setUp(self):
        super(TestGameSessionManager, self).setUp()
        GameSessionManager.USER_CURRENTLY_PLAYING = list()

    def tearDown(self):
        super(TestGameSessionManager, self).tearDown()

    def test_handle_user_update_user_exist_and_start_playing(self):
        # test user exist
        before_user_mock = MagicMock(id=1, name="user1", activity=None)
        after_activity_mock = MagicMock(name="activity1")
        after_user_mock = MagicMock(id=1, name="user1", activity=after_activity_mock)

        target_user = DiscordUser.get(id=1)
        self.assertIsNone(target_user.current_playing_session_start_time)
        GameSessionManager.handle_user_update(before_user_mock, after_user_mock)
        target_user = target_user.refresh()
        self.assertIsNotNone(target_user.current_playing_session_start_time)

    def test_handle_user_update_user_does_not_exist_and_start_playing(self):
        # test not exist
        before_user_mock = MagicMock(id=2, name="user2", activity=None)
        after_activity_mock = MagicMock(name="activity2")
        after_user_mock = MagicMock(id=2, name="user2", activity=after_activity_mock)

        with self.assertRaises(DiscordUser.DoesNotExist):
            DiscordUser.get(id=2)
        GameSessionManager.handle_user_update(before_user_mock, after_user_mock)
        target_user = DiscordUser.get(id=2)
        self.assertIsNotNone(target_user.current_playing_session_start_time)
        self.assertIsNone(target_user.current_playing_session_stop_time)

    def test_handle_user_update_user_stop_playing_but_was_not_tracked_yet(self):
        # user exist, was not tracked (not present in USER_CURRENTLY_PLAYING), stopped playing
        activity_mock = MagicMock(name="activity1")
        before_user_mock = MagicMock(id=1, name="user1", activity=activity_mock)
        after_user_mock = MagicMock(id=1, name="user1", activity=None)
        GameSessionManager.handle_user_update(before_user_mock, after_user_mock)
        target_user = DiscordUser.get(id=1)
        self.assertIsNone(target_user.current_playing_session_start_time)
        self.assertIsNone(target_user.current_playing_session_stop_time)

    def test_handle_user_update_user_stop_playing_was_tracked(self):
        activity_mock = MagicMock(name="activity1")
        before_user_mock = MagicMock(id=1, name="user1", activity=activity_mock)
        after_user_mock = MagicMock(id=1, name="user1", activity=None)
        GameSessionManager.USER_CURRENTLY_PLAYING = [1]
        target_user = DiscordUser.get(id=1)
        # set a session that has started before
        now = datetime.datetime.now()
        hour = datetime.timedelta(hours=1)
        date_1_hour_before = now - hour
        target_user.current_playing_session_start_time = date_1_hour_before
        target_user.save()

        # get number of session for this user
        all_session = models.GameSession.select().join(DiscordUser).where(DiscordUser.id == target_user.id)
        expected_session_after_update = len(all_session) + 1  # we should have one more session
        GameSessionManager.handle_user_update(before_user_mock, after_user_mock)
        target_user = target_user.refresh()
        self.assertIsNotNone(target_user.current_playing_session_stop_time)
        # we should now have one more session
        all_session = models.GameSession.select().join(DiscordUser).where(DiscordUser.id == target_user.id)
        self.assertEqual(expected_session_after_update, len(all_session))
        self.assertEqual(len(GameSessionManager.USER_CURRENTLY_PLAYING), 0)

    def test_handle_user_update_user_still_playing(self):
        activity_mock = MagicMock(name="activity1")
        before_user_mock = MagicMock(id=1, name="user1", activity=activity_mock)
        after_user_mock = MagicMock(id=1, name="user1", activity=activity_mock)
        GameSessionManager.USER_CURRENTLY_PLAYING = [1]
        GameSessionManager.handle_user_update(before_user_mock, after_user_mock)
        target_user = DiscordUser.get(id=1)
        # we should have no change
        self.assertIsNone(target_user.current_playing_session_start_time)
        self.assertIsNone(target_user.current_playing_session_stop_time)

    def test_get_top_rank_last_week(self):
        expected_result = [('test_user2', 2), ('test_user', 1)]
        self.assertEqual(expected_result, GameSessionManager.get_top_rank_last_week())

    def test_get_sorted_tuple(self):
        test_dict = {'test_user': 60, 'test_user2': 120, 'test_user3': 12}
        expected_result = [('test_user2', 120), ('test_user', 60), ('test_user3', 12)]
        self.assertEqual(expected_result, GameSessionManager.get_sorted_tuple(test_dict))
