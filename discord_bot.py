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
client = discord.Client()


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


def no_luck():
    """
    Return True following a percentage of chance
    :return:
    """
    chance = random.randint(1, 100)
    if chance < chance_to_troll:
        return True
    return False


@client.event
async def on_voice_state_update(before, after):
    """
    when a Member changes their voice state.
    """
    if after.voice.voice_channel is not None:
        # don't do it in AFK chan
        if after.voice_channel.name == "AFK":
            return

        if after.id == bot_id:  # do not troll the bot itself
            return

    if after.voice_channel is not None:
        print("name: %s,  ID: %s joined %s" % (after.name, after.id, after.voice.voice_channel.name))
        # only troll if he was not already in this chan
        if before.voice_channel is None or before.voice_channel.name != after.voice_channel.name:
            if not client.is_voice_connected(client.get_server(server_id)):
                if no_luck():
                    print("No luck, troll him!")
                    # get the voice chanel
                    voice = await client.join_voice_channel(after.voice.voice_channel)

                    # get random sound path
                    random_sound_path = get_random_sound_path(get_list_sound(sounds_path))
                    player = voice.create_ffmpeg_player(random_sound_path)
                    player.start()
                    while player.is_playing():
                        time.sleep(2)
                    print("end playing")

                    # stop voice
                    await voice.disconnect()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)
    try:
        client.run(discord_token)
    finally:
        client.close()
        client.logout()
        print("Exiting")
