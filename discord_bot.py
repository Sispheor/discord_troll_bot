# authorize bot
# https://discordapp.com/oauth2/authorize?&client_id=<my_id>&scope=bot&permissions=0
# apt install ffmpeg
import os
import signal

import discord as discord

from database_loader import get_database
from models.discord_user import DiscordUser
from models.game_session import GameSession
from my_discord_client import MyClient
import logging
client = None


def init_logger():
    logger = logging.getLogger('discord_bot')
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def init_database():
    print("Init database")
    db = get_database("troll_bot")
    db.connect()
    db.create_tables([DiscordUser, GameSession])
    db.close()
    print("Init database... done")


def main():
    logger = logging.getLogger('discord_bot')
    logger.info("Start Discord Troll Bot")
    server_id = os.getenv('DISCORD_SERVER_ID', None)
    bot_id = os.getenv('DISCORD_BOT_ID', None)
    discord_token = os.getenv('DISCORD_TOKEN', None)
    mysql_host = os.getenv('MYSQL_HOST', "127.0.0.1")
    mysql_user = os.getenv('MYSQL_USER', None)
    mysql_password = os.getenv('MYSQL_PASSWORD', None)
    mysql_database = os.getenv('MYSQL_DATABASE', None)

    if server_id is None:
        print("You must provide a 'DISCORD_SERVER_ID'")
        exit(1)
    if bot_id is None:
        print("You must provide a 'DISCORD_BOT_ID'")
        exit(1)
    if discord_token is None:
        print("You must provide a 'DISCORD_TOKEN'")
        exit(1)
    if mysql_user is None:
        print("You must provide a 'MYSQL_USER'")
        exit(1)
    if mysql_password is None:
        print("You must provide a 'MYSQL_PASSWORD'")
        exit(1)
    if mysql_host is None:
        print("You must provide a 'MYSQL_HOST'")
        exit(1)
    if mysql_database is None:
        print("You must provide a 'MYSQL_DATABASE'")
        exit(1)
    logger.info("DISCORD_SERVER_ID: %s" % server_id)
    logger.info("DISCORD_BOT_ID: %s" % bot_id)

    intents = discord.Intents.default()
    intents.typing = False
    intents.members = True
    intents.presences = True
    client = MyClient(intents=intents)
    client.run(discord_token)


def handle_exit():
    print("Clean exit")
    if client is not None:
        client.change_presence(status=discord.Status.offline)
        client.logout()
        client.close()
        print("Disconnected")


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    init_logger()
    init_database()
    main()

