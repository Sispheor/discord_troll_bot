# authorize bot
# https://discordapp.com/oauth2/authorize?&client_id=<my_id>&scope=bot&permissions=0
# apt install ffmpeg
import os
import signal

import discord as discord

from database_loader import DatabaseLoader
from models import DiscordUser, GameSession
from my_discord_client import MyClient

client = None


def init_database():
    db = DatabaseLoader.get_database("troll_bot")
    db.connect()
    db.create_tables([DiscordUser, GameSession])


def main():
    print("# Discord Troll Bot \n")
    server_id = os.getenv('DISCORD_SERVER_ID', None)
    bot_id = os.getenv('DISCORD_BOT_ID', None)
    discord_token = os.getenv('DISCORD_TOKEN', None)

    if server_id is None:
        print("You must provide a 'DISCORD_SERVER_ID'")
        exit(1)
    if bot_id is None:
        print("You must provide a 'DISCORD_BOT_ID'")
        exit(1)
    if discord_token is None:
        print("You must provide a 'DISCORD_TOKEN'")
        exit(1)

    print("DISCORD_SERVER_ID: %s" % server_id)
    print("DISCORD_BOT_ID: %s" % bot_id)

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
    init_database()
    main()

