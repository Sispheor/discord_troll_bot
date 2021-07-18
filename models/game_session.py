from peewee import ForeignKeyField, DateTimeField, IntegerField
from models.discord_user import DiscordUser
from models.base_model import BaseModel


class GameSession(BaseModel):
    discord_user = ForeignKeyField(DiscordUser, backref='game_sessions')
    session_start_time = DateTimeField()
    session_stop_time = DateTimeField()
    session_duration_minutes = IntegerField()
