import datetime
import logging
import operator

from database_loader import DatabaseLoader
from models import DiscordUser
from settings_loader import SettingLoader

logger = logging.getLogger('discord_bot')
db = DatabaseLoader.get_database()


class GameSessionManager:

    USER_CURRENTLY_PLAYING = []

    @classmethod
    @db.connection_context()
    def get_or_create_user(cls, user_id, name):
        try:
            target_user = DiscordUser.get(id=user_id)
            # update the name if changed
            target_user.name = name
            target_user.save()
        except DiscordUser.DoesNotExist:
            logger.info("Adding new user to database: '{}'".format(name))
            target_user = DiscordUser.create(id=user_id, name=name)

        return target_user

    @classmethod
    @db.connection_context()
    def handle_user_update(cls, before, after):
        if before.id in cls.USER_CURRENTLY_PLAYING:  # the user was playing
            if after.activity is not None:  # the user still playing
                logger.info("[Still playing] user: {}, activity: {}".format(after.name, after.activity.name))
            else:  # the user stopped playing
                logger.info("[Stopped playing] user: {}".format(after.name))
                cls.USER_CURRENTLY_PLAYING.remove(before.id)
                target_user = DiscordUser.get(id=after.id)
                target_user.stop_playing()
        else:  # the user was not playing
            if after.activity is not None:  # the user is now playing
                if after.activity.name in SettingLoader().settings.rank_non_tacked_game_name:
                    logger.info("[Session skipped] Application name '{}' not tracked".format(after.activity.name))
                else:
                    logger.info("[Started playing] user: '{}', "
                                "activity name: '{}'".format(after.name,
                                                             after.activity.name))
                    cls.USER_CURRENTLY_PLAYING.append(after.id)
                    target_user = cls.get_or_create_user(user_id=after.id, name=after.name)
                    target_user.start_playing()
            else:
                logger.info("[Session skipped] User '{}' stopped playing "
                            "but was not tracked yet".format(after.name))

    @classmethod
    @db.connection_context()
    def get_top_rank_last_week(cls):
        """
        return a sorted list of player with their hours played
        [('test_user2', 120), ('test_user', 60), ('test_user3', 12)]
        """
        today = datetime.datetime.now()
        logger.debug("[Top rank] Date now is: {}".format(today))
        days = datetime.timedelta(days=7)
        date_limit = today - days
        logger.debug("[Top rank] Date limit is: {}".format(date_limit))
        user_dict = dict()
        for discord_user in DiscordUser.select():
            all_session_for_this_user = discord_user.get_all_session_since_date(date_in_past=date_limit)
            total_played_minutes = discord_user.get_total_played_minute_for_session_list(all_session_for_this_user)
            total_played_hours = 0
            if total_played_minutes != 0:
                total_played_hours = round(total_played_minutes / 60)
            user_dict[discord_user.name] = total_played_hours
        return cls.get_sorted_tuple(user_dict)

    @staticmethod
    def get_sorted_tuple(dict_user):
        return sorted(dict_user.items(), key=operator.itemgetter(1), reverse=True)
