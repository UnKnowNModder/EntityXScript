""" client-related utility """
from __future__ import annotations
import bascenev1 as bs
import utils
from types import Authority
from typing import override

class ClientPlayer:
	""" the related player to the given Client. """
	def __init__(self, player: bs.SessionPlayer) -> None:
		self.player = player
	
	def handle(self, message) -> None:
		""" handles message for the player. """
		player = self.player.activityplayer
		if not player.actor:
			return
		player.actor.node.handlemessage(message)
	
	def remove(self) -> None:
		""" removes the player from game. """
		self.player.remove_from_game()
	
	def profiles(self) -> list[str]:
		""" returns the profiles of the session player.. """
		return self.player.inputdevice.get_player_profiles()
	
	def kill(self) -> None:
		self.handle(bs.DieMessage())
	
	def freeze(self) -> None:
		self.handle(bs.FreezeMessage())
	
	def thaw(self) -> None:
		self.handle(bs.ThawMessage())

class Client:
	""" Client class for multiple features at one place. """
	__mute_clients = set() # class level var
	def __init__(
		self, client_id: int = 0, account_id: str = "", name: str = "", is_v2: bool = True, in_lobby: bool = True
	) -> None:
		self.client_id = client_id
		self.account_id = account_id
		self.name = name
		self.is_v2 = is_v2
		self.in_lobby = in_lobby

	@property
	def player(self) -> ClientPlayer | None:
		""" returns the ClientPlayer associated with this client.. """
		for splayer in bs.get_foreground_host_session().sessionplayers:
			if splayer.inputdevice.client_id == self.client_id:
				return ClientPlayer(splayer)
		return
	
	@property
	def authority(self) -> Authority:
		""" this client's authority level. """
		if self.client_id == -1:
			# special access to server.
			return Authority.HOST
		return bs.storage.roles.get_authority_level(self.account_id)
	
	@property
	def is_mute(self) -> bool:
		""" returns whether the client is mute or not. """
		return self.account_id in Client.__mute_clients
	
	def mute(self) -> None:
		""" mute this client. """
		if self.account_id not in Client.__mute_clients:
			Client.__mute_clients.add(self.account_id)
			return True
		# already mute.
	
	def unmute(self) -> None:
		""" unmute this client. """
		if self.account_id in Client.__mute_clients:
			Client.__mute_clients.discard(self.account_id)
			return True
		# not mute.
	
	def kick(self, time: int = 300) -> None:
		""" kick this client. """
		bs.disconnect_client(self.client_id, ban_time = time)

	def success(self, message: str) -> None:
		""" show this client a success message. """
		utils.success(message, clients = [self.client_id])
	
	def error(self, message: str) -> None:
		""" show this client an error message. """
		utils.error(message, clients = [self.client_id])
	
	def send(self, message: str, sender: str | None) -> None:
		""" show this client a chat message. """
		utils.send(message, clients = [self.client_id], sender = sender)

class Dummy(Client):
	""" dummy client. """
	def __init__(self, client_id: int, account_id: str) -> None:
		self.client_id = client_id
		self.account_id = account_id


def get_clients() -> list[Client]:
	"""returns a list of Client object. """
	clients = []
	for client in bs.get_game_roster()[1:]:
		client_id = client["client_id"]
		account_id = client["account_id"]
		spec_string = eval(client["spec_string"])
		name = spec_string["n"]
		# handle for pc players..
		if spec_string["a"].lower() == "local" and name.startswith("PC"):
			is_v2 = True
		else:
			is_v2 = spec_string["a"] == "V2"
		in_lobby = not client["players"]
		if not in_lobby:
			name = client["players"][0]["name"]
		else:
			name = client["display_string"]
		clients.append(Client(client_id, account_id, name, is_v2, in_lobby))
	return clients

def get_client(client_id: int | str) -> Client | None:
	""" fetches and returns a Client class based on the client_id. """
	# manual converting to avoid str cases.
	client_id = int(client_id)
	for client in get_clients():
		if client.client_id == client_id:
			return client
	return