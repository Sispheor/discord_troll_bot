# authorize bot
# https://discordapp.com/oauth2/authorize?&client_id=<my_id>&scope=bot&permissions=0
# apt install ffmpeg
import glob
import os
import random
import signal
import sys

import discord as discord

from database_loader import DatabaseLoader
from models import DiscordUser, GameSession
from my_discord_client import MyClient


def sigterm_handler(_signo, _stack_frame):
    print("sigterm_handler executed, %s, %s" % (_signo, _stack_frame))
    sys.exit(0)


def get_list_sound(path_to_list):
    return glob.glob(path_to_list + os.sep + "*")


def get_random_sound_path(list_sound):
    return random.choice(list_sound)


def init_database():
    db = DatabaseLoader.get_database("troll_bot")
    db.connect()
    db.create_tables([DiscordUser, GameSession])


def main():
    server_id = os.getenv('DISCORD_SERVER_ID', None)
    bot_id = os.getenv('DISCORD_BOT_ID', None)
    discord_token = os.getenv('DISCORD_TOKEN', None)
    sounds_path = os.getenv('SOUNDS_PATH', "sounds/")
    chance_to_troll = os.getenv('CHANCE_TO_TROLL', 20)
    if server_id is None:
        print("You must provide a 'DISCORD_SERVER_ID'")
        exit(1)
    if bot_id is None:
        print("You must provide a 'DISCORD_BOT_ID'")
        exit(1)
    if discord_token is None:
        print("You must provide a 'DISCORD_TOKEN'")
        exit(1)
    try:
        chance_to_troll = int(chance_to_troll)
        if chance_to_troll > 100 or chance_to_troll < 1:
            raise ValueError
    except ValueError:
        print("Not a valid 'CHANCE_TO_TROLL'. Must be between 1 and 100")
        exit(1)

    print("DISCORD_SERVER_ID: %s" % server_id)
    print("DISCORD_BOT_ID: %s" % bot_id)
    print("SOUND_PATH: %s" % sounds_path)
    print("CHANCE_TO_TROLL: %s" % chance_to_troll)

    print('Start discord client')
    intents = discord.Intents.default()
    intents.typing = False
    intents.members = True
    intents.presences = True
    client = MyClient(intents=intents)
    client.run(discord_token)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)
    init_database()
    main()

