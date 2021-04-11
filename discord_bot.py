# authorize bot
# https://discordapp.com/oauth2/authorize?&client_id=<my_id>&scope=bot&permissions=0
# apt install ffmpeg
import glob
import os
import random
import signal
import sys
import time
import discord as discord
from peewee import SqliteDatabase

from database_loader import DatabaseLoader
from game_session_manager import GameSessionManager
from models import DiscordUser, GameSession

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

intents = discord.Intents.default()
intents.typing = False
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)


def sigterm_handler(_signo, _stack_frame):
    print("sigterm_handler executed, %s, %s" % (_signo, _stack_frame))
    sys.exit(0)


def get_list_sound(path_to_list):
    return glob.glob(path_to_list + os.sep + "*")


def get_random_sound_path(list_sound):
    return random.choice(list_sound)


@client.event
async def on_ready():
    print("Logged in as '%s'" % client.user.name)
    print("Client id: %s" % client.user.id)
    print("")


def no_luck():
    """
    Return True following a percentage of chance
    :return:
    """
    chance = random.randint(1, 100)
    if chance < chance_to_troll:
        return True
    return False


# @client.event
# async def on_voice_state_update(member, before, after):
#     """
#     when a Member changes their voice state.
#     """
#     if member.voice is not None:
#         # don't do it in AFK chan
#         if member.voice.afk:
#             print("afk")
#             return
#
#         if member.id == bot_id:  # do not troll the bot itself
#             return
#
#     if after.channel is not None:
#         print("Member '%s' joined %s" % (member.name, after.channel.name))
#         # only troll if he was not already in this chan
#         if before.channel is None or before.channel.name != after.channel.name:
#
#             if no_luck():
#                 print("No luck, troll him!")
#                 if after.channel not in (x.channel.name for x in client.voice_clients):
#                     # connect to the channel
#                     vc = await after.channel.connect()
#                     # get random sound path
#                     random_sound_path = get_random_sound_path(get_list_sound(sounds_path))
#                     vc.play(discord.FFmpegPCMAudio(random_sound_path), after=lambda e: print('done', e))
#                     while vc.is_playing():
#                         time.sleep(2)
#                     print("End playing")
#                     # stop voice
#                     await vc.disconnect()
NOT_FOLLOWED_ID = [719806770133991434]  # epic game bot
USER_CURRENTLY_PLAYING = list()


@client.event
async def on_member_update(before, after):
    if before.id not in NOT_FOLLOWED_ID:
        print("[User update] name: {}, id: {}".format(before.name, before.id))
        GameSessionManager.handle_user_update(before, after)


def init_database():
    db = DatabaseLoader.get_database("troll-bot.db")
    db.connect()
    db.create_tables([DiscordUser, GameSession])


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)
    try:
        init_database()
        client.run(discord_token)
    except KeyboardInterrupt:
        client.close()
        client.loop.run_until_complete(client.logout())
        print("Exit")
    finally:
        client.loop.close()
