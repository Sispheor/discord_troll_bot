import datetime
import operator

from models import DiscordUser


class GameSessionManager:

    USER_CURRENTLY_PLAYING = []

    @classmethod
    def get_or_create_user(cls, user_id, name):
        try:
            target_user = DiscordUser.get(id=user_id)
            # update the name if changed
            target_user.name = name
            target_user.save()
        except DiscordUser.DoesNotExist:
            print("Adding new user to database: '{}'".format(name))
            target_user = DiscordUser.create(id=user_id, name=name)

        return target_user

    @classmethod
    def handle_user_update(cls, before, after):
        if before.id in cls.USER_CURRENTLY_PLAYING:  # the user was playing
            if after.activity is not None:  # the user still playing
                print("[Still playing] name: {}, id: {}".format(after.name, after.id))
            else:  # the user stopped playing
                print("[Stopped playing] name: {}, id: {}".format(after.name, after.id))
                cls.USER_CURRENTLY_PLAYING.remove(before.id)
                target_user = DiscordUser.get(id=after.id)
                target_user.stop_playing()
        else:  # the user was not playing
            if after.activity is not None:  # the user is now playing
                print("[Started playing] name: {}, activity name: {}, activity id: {}".format(after.name,
                                                                                              after.activity.name,
                                                                                              after.activity.application_id))
                cls.USER_CURRENTLY_PLAYING.append(after.id)  # keep a in memory list so we do not call the db everytime
                target_user = cls.get_or_create_user(user_id=after.id, name=after.name)
                target_user.start_playing()
            else:
                print("[Session skipped] User '{}' stopped playing but was not tracked yet".format(after.name))

    @classmethod
    def get_top_rank_last_week(cls):
        """
        return a sorted list of player with their hours played
        [('test_user2', 120), ('test_user', 60), ('test_user3', 12)]
        """
        today = datetime.datetime.now()
        print("Date now is: {}".format(today))
        days = datetime.timedelta(days=7)
        date_limit = today - days
        print("Date limit is: {}".format(date_limit))
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
