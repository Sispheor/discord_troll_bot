import aiocron
import discord

from game_session_manager import GameSessionManager

NOT_FOLLOWED_ID = [719806770133991434]  # epic game bot


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        print('Start cronjob')
        cron = aiocron.crontab('* * * * *', func=self.cronjob_print_rank_in_channel, start=False)
        cron.start()

    async def on_ready(self):
        print("Logged in as '%s'" % self.user.name)
        print("Client id: %s" % self.user.id)
        print("")

    async def cronjob_print_rank_in_channel(self):
        print("Cronjob cronjob_print_rank_in_channel start")
        channel_id = 742095331004514385  # general
        target_channel = self.get_channel(channel_id)
        top_players = GameSessionManager.get_top_rank_last_week()
        master_fapper_name = top_players[0][0]
        await target_channel.send("Master fapper of the week: :trophy: **{}** :trophy: ".format(master_fapper_name))
        await target_channel.send(self.get_tabulate_rank(top_players))
        print("Cronjob cronjob_print_rank_in_channel complete")
    # def no_luck():
    #     """
    #     Return True following a percentage of chance
    #     :return:
    #     """
    #     chance = random.randint(1, 100)
    #     if chance < chance_to_troll:
    #         return True
    #     return False

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

    async def on_member_update(self, before, after):
        if before.id not in NOT_FOLLOWED_ID:
            print("[User update] name: {}, id: {}".format(before.name, before.id))
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
