import discord
from discord.ext import commands
from discord import app_commands
import bacore
import babase


class EntityBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="e!", intents=discord.Intents.default())

    async def on_ready(self):
        print(f'Logged in as {self.user.name} - {self.user.id}')

    async def on_message(self, message):
        """Check messages if sent by itself return None else process the command (if any)"""
        if message.author == self.user:
            return
        await self.process_commands(message)
     
    """To check bot response"""
    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send('Pong!')

    """Creates a slash command group named match so we can use commands like /match add..."""
    match_group = app_commands.Group(name='match', description='Match Management')

    @match_group.command(name='add',description='Appoint a match')
    async def match_add(self, interaction: discord.Interaction, series_count: int, team_name1: str, team_name2: str, team1_players: str, team2_players: str):
        try:
            match = {}
            match["series"] = int(series_count)
            match["team1"] = {}
            match["team1"][team_name1] = list(eval(team1_players))
            match["team2"] = {}
            match["team2"][team_name2] = list(eval(team2_players))
            bacore.tournament.insert(match)
            await interaction.response.send_message("Match Appointed")
        except Exception as e:
            await interaction.response.send_message(e)
            pass

def start_bot():
    bot = EntityBot()
    bot.run("Enter Your Fuking Bot Token Here")

# ba_meta import babase.Plugin
class BotPlugin(babase.plugin):
    def __init__(self):
        start_bot()
        