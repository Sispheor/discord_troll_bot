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
            DiscordUser.create(id=user_id, name=name)
            target_user = DiscordUser.get(id=user_id)

        return target_user

    @classmethod
    def handle_user_update(cls, before, after):
        if before.id in cls.USER_CURRENTLY_PLAYING:  # the user was playing
            if after.activity is not None:  # the user still playing
                print("User {} still playing".format(before.name))
            else:  # the user stopped playing
                print("User {} stopped playing".format(before.name))
                cls.USER_CURRENTLY_PLAYING.remove(before.id)
                target_user = DiscordUser.get(id=after.id)
                target_user.stop_playing()
        else:  # the user was not playing
            if after.activity is not None:  # the user is now playing
                print("User {} started playing '{}'".format(after.name, after.activity.name))
                cls.USER_CURRENTLY_PLAYING.append(after.id)  # keep a in memory list so we do not call the db everytime
                target_user = cls.get_or_create_user(user_id=after.id, name=after.name)
                target_user.start_playing()
            else:
                print("User {} stopped playing but was not tracked yet. Session is skipped")
