""" config storage core. """
from __future__ import annotations
import os
from ._storage import Storage
from ._enums import Utility, Playlist

class Config(Storage):
	"""config storage class."""

	def __init__(self) -> None:
		super().__init__("config.json")
		self.toml = os.path.join(
			f"{os.sep}".join(os.getcwd().split(os.sep)[:-1]), "config.toml"
		)
		self.bootstrap()

	def bootstrap(self) -> None:
		"""creates essential files."""
		if not os.path.exists(self.path):
			config = {}
			config[Utility.WHITELIST] = False
			config[Utility.SPECTATOR] = True
			self.commit(config)

	def toggle(self, utility: Utility) -> bool:
		"""toggles the utility."""
		config = self.read()
		if not utility in config:
			config[utility] = True
		config[utility] = not config[utility]
		self.commit(config)
		return config[utility]

	def set_playlist(self, playlist: Playlist) -> None:
		"""changes the playlist code in .toml file."""
		code = playlist.value
		with open(self.toml, "r") as f:
			lines = f.readlines()
		with open(self.toml, "w") as f:
			for line in lines:
				if line.strip().startswith(f"playlist_code ="):
					f.write(f"playlist_code = {code}\n")
				else:
					f.write(line)

	@property
	def whitelist(self) -> bool:
		"""returns whether whitelist is enable or not."""
		config = self.read()
		if Utility.WHITELIST not in config:
			config[Utility.WHITELIST] = False
		return config[Utility.WHITELIST]

	@property
	def spectator(self) -> bool:
		"""returns whether spectator is enable or not."""
		config = self.read()
		if Utility.SPECTATOR not in config:
			config[Utility.SPECTATOR] = True
		return config[Utility.SPECTATOR]