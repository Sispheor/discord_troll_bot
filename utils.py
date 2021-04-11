

def get_played_session_minute(playing_session_start_time, playing_session_stop_time):
    time_delta = (playing_session_stop_time - playing_session_start_time)
    total_seconds = time_delta.total_seconds()
    minutes = total_seconds / 60
    return minutes
