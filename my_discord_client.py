import glob
import os
import random
import time

import aiocron
import discord

from game_session_manager import GameSessionManager
from settings_loader import SettingLoader


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('Start discord client')
        self.settings = SettingLoader().settings
        self.bot_id = os.getenv('DISCORD_BOT_ID', None)

    async def on_ready(self):
        print("Logged in as '%s'" % self.user.name)
        print("Client id: %s" % self.user.id)
        print("")
        if self.settings.rank_enabled:
            print('Start cronjob with settings: {}'.format(self.settings.rank_cron_string))
            cron = aiocron.crontab(self.settings.rank_cron_string, func=self.cronjob_print_rank_in_channel, start=False)
            cron.start()

        self.print_current_user_activities()

    async def cronjob_print_rank_in_channel(self):
        print("Cronjob cronjob_print_rank_in_channel start")
        channel_id = self.settings.rank_channel_id
        target_channel = self.get_channel(channel_id)
        top_players = GameSessionManager.get_top_rank_last_week()
        master_fapper_name = top_players[0][0]
        embed = discord.Embed(title="Master fapper", color=0x109319)
        embed.add_field(name="Master fapper of the week",
                        value=":trophy: **{}** :trophy:".format(master_fapper_name),
                        inline=False)
        output = ("```" + "\n\n" + self.get_tabulate_rank(top_players) + "```")
        embed.add_field(name="Fappers list", value=output,
                        inline=False)
        await target_channel.send(embed=embed)
        print("Cronjob cronjob_print_rank_in_channel complete")

    def no_luck(self):
        """
        Return True following a percentage of chance
        :return:
        """
        chance = random.randint(1, 100)
        if chance < self.settings.chance_to_troll:
            return True
        return False

    async def on_voice_state_update(self, member, before, after):
        """
        when a Member changes their voice state.
        """
        if not self.settings.troll_member_when_join_channel:
            return
        if member.voice is not None:
            # don't do it in AFK chan
            if member.voice.afk:
                print("afk")
                return

            if member.id == self.bot_id:  # do not troll the bot itself
                return

        if after.channel is not None:
            print("Member '%s' joined %s" % (member.name, after.channel.name))
            # only troll if he was not already in this chan
            if before.channel is None or before.channel.name != after.channel.name:

                if self.no_luck():
                    print("No luck, troll him!")
                    if after.channel not in (x.channel.name for x in self.voice_clients):
                        # connect to the channel
                        vc = await after.channel.connect()
                        # get random sound path
                        random_sound_path = self.get_random_sound_path(self.get_list_sound(self.settings.sounds_path))
                        vc.play(discord.FFmpegPCMAudio(random_sound_path), after=lambda e: print('done', e))
                        while vc.is_playing():
                            time.sleep(2)
                        print("End playing")
                        # stop voice
                        await vc.disconnect()

    async def on_member_update(self, before, after):
        if before.id not in self.settings.rank_non_tracked_user_id:
            print("[User update] name: {}, id: {}".format(before.name, before.id))
            if after.activity is not None and after.activity.application_id not in self.settings.rank_non_tacked_game_id:
                GameSessionManager.handle_user_update(before, after)

    @staticmethod
    def get_tabulate_rank(sorted_player_list):
        from tabulate import tabulate
        headers = ["Player", "Hours"]
        table = list()
        for player in sorted_player_list:
            user_line_list = [player[0], player[1]]
            table.append(user_line_list)
        return tabulate(table, headers, tablefmt="simple")

    @staticmethod
    def get_list_sound(path_to_list):
        return glob.glob(path_to_list + os.sep + "*")

    @staticmethod
    def get_random_sound_path(list_sound):
        return random.choice(list_sound)

    def print_current_user_activities(self):
        print("# Current connected users")
        for member in self.get_all_members():
            if member.activity is not None:
                print("User name: {}, id: {}. Activity name: {}, id: {}".format(member.name,
                                                                                member.id,
                                                                                member.activity.name,
                                                                                member.activity.application_id))
