import datetime
import logging

from peewee import *

from models.base_model import BaseModel
from utils import get_played_session_minute

logger = logging.getLogger('discord_bot')


class DiscordUser(BaseModel):
    id = BigIntegerField(primary_key=True)
    name = CharField()
    current_playing_session_start_time = DateTimeField(null=True)
    current_playing_session_stop_time = DateTimeField(null=True)

    def refresh(self):
        return type(self).get(self._pk_expr())

    def start_playing(self):
        self.current_playing_session_start_time = datetime.datetime.now()
        self.current_playing_session_stop_time = None
        self.save()

    def stop_playing(self):
        self.current_playing_session_stop_time = datetime.datetime.now()
        # calculate time in minute of the played session
        played_session_minute = get_played_session_minute(self.current_playing_session_start_time,
                                                          self.current_playing_session_stop_time)
        logger.debug("[Playing session saved] User '{}' "
                     "played a session of {} minutes".format(self.name,
                                                             round(played_session_minute)))
        from models.game_session import GameSession
        GameSession.create(discord_user=self,
                           session_start_time=self.current_playing_session_start_time,
                           session_stop_time=self.current_playing_session_stop_time,
                           session_duration_minutes=played_session_minute)
        self.save()

    def get_all_session_since_date(self, date_in_past):
        """
        Given a date in the past and a user, retrieve the sum of played session
        """
        # Get days that have events for the current month.
        from models.game_session import GameSession
        all_session = GameSession.select().join(DiscordUser).where(
            (GameSession.session_start_time >= date_in_past) &
            (DiscordUser.id == self.id))
        return all_session

    @staticmethod
    def get_total_played_minute_for_session_list(session_list):
        total_played_minutes = 0
        for session in session_list:
            total_played_minutes += session.session_duration_minutes
        return total_played_minutes
