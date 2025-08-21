import discord
from discord.ext import commands
from discord import app_commands
import bacore
import babase
import bascenev1
import traceback
import typing


class EntityBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="e!", intents=discord.Intents.default(), owner_id=924617239301324856)

    async def on_ready(self):
        print(f'Logged in as {self.user.name} - {self.user.id}')

    async def on_message(self, message):
        """Check messages if sent by itself return None else process the command (if any)"""
        if message.author == self.user:
            return
        await self.process_commands(message)

    """Add or remove a discord user to owner list"""
    @commands.command(name='owner')
    @commands.is_owner() # Check if ctx.user is bot owner
    async def owner(self, ctx, user: discord.Member):
        try:
            if bacore.roles.has_role(LEADER, user.id):
                bacore.roles.remove(LEADER, user.id)
                await self.ctx.send(f"{user.name}[`{user.id}`] Removed from Role: LEADER")
            else:
                bacore.roles.add(Roles.OWNER, user.id)
                await ctx.send(f"{user.name}[`{user.id}`] Added Role: LEADER")
        except Exception as e:
            traceback_msg = traceback.format_exc()
            print(traceback_msg)
            await ctx.send(traceback_msg)
            
         
     
    """Sync slash commands"""
    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: typing.Optional[typing.Literal["~", "*", "^"]] = None) -> None:
        if not guilds:
            if spec == "~":

                synced = await ctx.bot.tree.sync(guild=ctx.guild)

            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)

                synced = await ctx.bot.tree.sync(guild=ctx.guild)

            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)

                await ctx.bot.tree.sync(guild=ctx.guild)

                synced = []

            else:

                synced = await ctx.bot.tree.sync()

            await ctx.send(f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}")



            return

        ret = 0

        for guild in guilds:

            try:

                await ctx.bot.tree.sync(guild=guild)

            except discord.HTTPException:

                pass

            else:

                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    """To check bot response"""
    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send('Pong!')

    """Increases the limit of server max players"""
    @commands.command(name='limit', description='Increase in-game max players limit')
    async def limit(ctx, limit: int):
        try:
            if bacore.roles.has_role(LEADER, ctx.author.id):
                bascenev1.pushcall(babase.chatmessage, message=f"/limit {limit}", sender_override=ctx.user.name,from_other_thread=True)
                await ctx.send(f"Set max-player limit to {limit}")
            else:
                await ctx.send('Access Denied')
        except Exception as e:
            traceback_msg = traceback.format_exc()
            await ctx.send(traceback_msg)
            print(traceback_msg)
            

    """Restart the server"""
    @commands.command(name='quit', description='Restart the server')
    async def quit(ctx):
        try:
            if bacore.roles.has_role(LEADER, ctx.author.id):
                await ctx.send('Restarting Server.\n[10%==========100%]')
                babase.quit()
            else:
                await ctx.send('Access Denied')
        except Exception as e:
            traceback_msg = traceback.format_exc()
            print(traceback_msg)
            await ctx.send(traceback_msg)
            
    

    """Creates a slash command group named match so we can use commands like /match add..."""
    match_group = app_commands.Group(name='match', description='Match Management')

    @match_group.command(name='add',description='Appoint a match')
    async def match_add(self, interaction: discord.Interaction, series_count: int, team_name1: str, team_name2: str, team1_players: str, team2_players: str):
        try:
            if bacore.roles.has_role(LEADER, interaction.user.id):
                match = {}
                match["series"] = int(series_count)
                match["team1"] = {}
                match["team1"][team_name1] = list(eval(team1_players))
                match["team2"] = {}
                match["team2"][team_name2] = list(eval(team2_players))
                bacore.tournament.insert(match)
                await interaction.response.send_message("Match Appointed")
            else:
                await interaction.response.send_message("Access Denied")
        except Exception as e:
            traceback_msg = traceback.format_exc()
            await interaction.response.send_message(traceback_msg)
            print(traceback_msg)
            

def start_bot():
    bot = EntityBot()
    bot.run("Enter Your Fuking Bot Token Here")

# ba_meta import babase.Plugin
class BotPlugin(babase.Plugin):
    def __init__(self):
        start_bot()
        