import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
import asyncio
import json
import typing
from typing import Literal
import os
import requests
import datetime
import traceback
import textwrap
import threading
import io
from contextlib import redirect_stdout
from serverfiles.config import get_data as settings
import serverfiles.config as config

class MyClient(commands.Bot):
    def __init__(self, *, intents: discord.Intents, application_id: int):
        super().__init__(
            intents=intents,
            application_id=application_id,
            command_prefix=commands.when_mentioned_or("*"),
            owner_id=924617239301324856,
        )

    async def setup_hook(self):
        try:
            print("will to-do later")
        except Exception as e:
            print(f"An error occured in setup_hook: {e}")
        

    async def on_ready(self):
        print(f"{self.user} is now online!")
        await self.load_extension("jishaku")

intents = discord.Intents.all()
intents.message_content = True
bot = MyClient(intents=intents, application_id=1238760771052245042)
setting = settings()
staff_cmds = ["send"]
no_perms = "Sorry! You aren't one of the staff team."

# Main Permission Handler
def is_owner():
    async def predicate(interaction: discord.Interaction) -> bool:
        return interaction.user.id == bot.owner_id
    return app_commands.check(predicate)

def perm_check(userid, type: Literal["leader", "staff"], cmd: str):
    staffs = setting["botdata"]["staff"]
    leaders = setting["botdata"]["leaders"]

    if str(userid) in leaders:
        return True
    elif str(userid) in staffs and type == "staff" and cmd in staff_cmds:
        return True
    else:
        return False

def check_pb(pb_id: str):
    url = requests.get(f"http://bombsquadgame.com/bsAccountInfo?buildNumber=20258&accountID={pb_id}")
    try:
        result = url.json()
        check = result["profileDisplayString"]
        return True, result
    except:
        return False, None

def get_acc_creation(pb_id: str):
    try:
        response = requests.get(f"https://legacy.ballistica.net/accountquery?id={pb_id}")
        data = response.json()
        cre_time = data["created"]
        return datetime.datetime(*map(int, cre_time))
    except Exception as e:
        print(f"Error: {e}")
        return "Unknown"
# Slash Command Error Handlers
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(f"You lack the required permissions: {error}", ephemeral=True)
    elif isinstance(error, app_commands.BotMissingPermissions):
        await interaction.response.send_message(f"I lack the required permissions: {error}", ephemeral=True)
    elif isinstance(error, app_commands.CommandInvokeError):
        await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)
        print(f"CommandInvokeError: {traceback.format_exc()}")
    else:
        await interaction.response.send_message(f"An unexpected error occurred: {error}", ephemeral=True)

# Message Command Error Handlers
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"You lack the required permissions: {error}")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send(f"I lack the required permissions: {error}")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send(f"An error occurred: {error}")
        print(f"CommandInvokeError: {traceback.format_exc()}")
    else:
        await ctx.send(f"An unexpected error occurred: {error}")

# Command: Eval
def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])
    return content.strip('` \n')

@bot.command(hidden=True, name="eval")
@commands.is_owner()
async def eval(ctx: commands.Context, *, body: str):
    """Evaluates Python code."""
    env = {
        "bot": bot,
        "ctx": ctx,
        "channel": ctx.channel,
        "author": ctx.author,
        "guild": ctx.guild,
        "message": ctx.message,
    }
    env.update(globals())
    body = cleanup_code(body)
    stdout = io.StringIO()
    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
    try:
        exec(to_compile, env)
    except Exception as e:
        return await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")
    func = env["func"]
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        await ctx.send(f"```py\n{value}{traceback.format_exc()}\n```")
    else:
        value = stdout.getvalue()
        try:
            await ctx.message.add_reaction("✅")
        except:
            pass
        if ret is None:
            if value:
                await ctx.send(f"```py\n{value}\n```")
        else:
            await ctx.send(f"```py\n{value}{ret}\n```")




async def start_bot():
    await bot.start("")

def run_thread(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

    asyncio.run_coroutine_threadsafe(start_bot(), loop)
    
def run():
    loop = asyncio.new_event_loop()
    threading.Thread(target=run_thread, args=(loop,)).start()
