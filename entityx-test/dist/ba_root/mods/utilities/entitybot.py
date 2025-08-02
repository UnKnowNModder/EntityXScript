import discord
from discord.ext import commands
import jishaku
import babase as ba, bascenev1 as bs

"""Main Bot Class"""
class MyClass(commands.Bot):
	def __init__(self, *,intents: discord.Intents):
		super().__init__(command_prefix=",", intents=intents,owner_id=924617239301324856)
		
	async def setup_hook(self):
		""" Load Extensions (Cogs) Files """
		try:
			await bot.load_extension("jishaku")
		except Exception as e:
			print(f"Error in setup_hook: {e}")
			pass
	
	async def on_ready(self):
		""" Check if bot is ready """
		print("Bot is online")

    async def start_bot(self):
    	await bot.start("")

    def run_thread(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()
        asyncio.run_coroutine_threadsafe(self.start_bot(), loop)
    
    def run(self):
        loop = asyncio.new_event_loop()
        threading.Thread(target=self.run_thread, args=(loop,)).start()
        