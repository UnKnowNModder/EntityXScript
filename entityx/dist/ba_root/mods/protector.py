""" Protects the server from unwanted players..
though I'm not unwanted :D (hope so)
"""

# ba_meta require api 9
from __future__ import annotations
import bascenev1 as bs
import babase as ba
from types import Role
from clients import get_clients

# ba_meta export plugin
class Protector(ba.Plugin):
	"""somewhat fishy name.."""
	def __init__(self):
		self.afk_time = 20 # seconds, + 10 will be added in code.
		self.lobby = {}

	def on_app_running(self):
		# delay to get a valid session..
		self.runner_loop_timer = bs.AppTimer(3, self.check_context)
	
	def check_context(self):
		session = bs.get_foreground_host_session()
		if session:
			with session.context:
				self.runner_loop_timer = bs.timer(1, ba.Call(self.runner_loop), repeat=True)
				print("Protector is on..")
		
	def runner_loop(self):
		"""this is the runner loop that protects everything.."""
		config = bs.storage.config
		roles = bs.storage.roles
		clients = get_clients()
		for client in clients:
			if client.authority:
				# no checks against authority.
				continue
			# Inspect: is client v2?
			if not client.is_v2:
				client.kick()
				continue
			
			# blacklist
			if roles.has_role(Role.BANLIST, client.account_id):
				# direct kick em, no message.
				client.kick()
				continue
			# whitelist
			if config.whitelist:
				# by default authority checks for whitelist, so this case is true for everybody who's not whitelisted.
				client.error(f"{client.name}, you are not in whitelist..")
				client.kick()
		if not config.spectator:
			self.handle_lobby_afk()

	def handle_lobby_afk(self):
		"""handles afk lobby players.."""
		clients = get_clients()
		for client in clients:
			# lobby afk
			client_id = client.client_id
			if client.in_lobby and client_id not in self.lobby:
				self.lobby[client_id] = 10 + self.afk_time
			elif not client.in_lobby and client_id in self.lobby:
				del self.lobby[client_id]
		for client in self.lobby.copy():
			self.lobby[client] -= 1
			if self.lobby[client] == 0:
				# kick the client..
				bs.broadcastmessage(
					"Kicking you for being idle in lobby for too long",
					color=(1, 0, 0),
					transient=True,
					clients=[client],
				)
				bs.disconnect_client(client)
				print(f"Kicked {client} for being afk in lobby")
				del self.lobby[client]
			elif self.lobby[client] <= self.afk_time:
				# start warnings..
				bs.broadcastmessage(
					f"You have {self.lobby[client]}s left, hurry up and join the game.",
					color=(1, 0, 0),
					transient=True,
					clients=[client],
				)

