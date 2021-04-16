

def get_played_session_minute(playing_session_start_time, playing_session_stop_time):
    time_delta = (playing_session_stop_time - playing_session_start_time)
    total_seconds = time_delta.total_seconds()
    minutes = total_seconds / 60
    return minutes


class Singleton(object):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance
