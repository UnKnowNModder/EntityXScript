import discord
from discord.ext import commands
from discord import app_commands
import bacore


class EntityBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="+", intents=discord.Intents.all())

    async def on_ready(self):
        print(f'Logged in as {self.user.name} - {self.user.id}')

    async def on_message(self, message):
        if message.author == self.user:
            return
        await self.process_commands(message)
        
    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send('Pong!')

    match_group = app_commands.Group(name='match', description='Match Management')

    @match_group.command(name='add',description='Add a match')
    async def match_add(self, interaction: discord.Interaction, series_count: int, team_name1: str, team_name2: str, team1_pbids: str, team2_pbids: str):
        try:
            team1_players = team1_pbids.split(',')
            team2_players = team2_pbids.split(',')
            if len(team1_players) or len(team2_players) < 4:
                await interaction.response.send_message("Enter equal players **4** in both teams")
            else:
                match = {"series": series_count, "team1": [team_name1, team1_players], "team2": [team_name2, team2_players]}
                bacore.tournament.insert(match)
                await interaction.response.send_message("Match Appointed")
        except Exception as e:
            await interaction.response.send_message(e)
            pass

def main():
    bot = EntityBot()
    bot.run()