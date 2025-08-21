import discord
from discord.ext import commands
from discord import app_commands
import bacore
import babase
import bascenev1


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

    """Increases the limit of server max players"""
    @commands.command(name='limit', description='Increase in-game max players limit')
    async def limit(ctx, limit: int):
        try:
            bascenev1.pushcall(babase.chatmessage, message=f"/limit {limit}", sender_override=ctx.user.name,from_other_thread=True)
            await ctx.send(f"Set max-player limit to {limit}")
        except Exception as e:
            traceback = traceback.print_exc()
            await ctx.send(traceback)
            print(traceback)

    """Restart the server"""
    @commands.command(name='quit', description='Restart the server')
    async def quit(ctx):
        try:
            await ctx.send('Restarting Server.\n[10%==========100%]')
            babase.quit()
        except Exception as e:
            traceback = traceback.print_exc()
            print(traceback)
            await ctx.send(traceback)
    

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
        