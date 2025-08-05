"""core package that initializes and binds storage methods."""

# ba_meta require api 9

import babase, sys
from ._config import Config
from ._roles import Roles
from ._tournament import Tournament
from ._clients import (
	Client,
	Player,
	Dummy,
	Players,
	all_clients,
	fetch_client,
	fetch_player
)
from ._utils import (
	success,
	error,
	send
)
from ._enums import (
	Authority,
	Role,
	Playlist,
	Utility,
	Match
)

# ba_meta export babase.Plugin
class Initialize(babase.Plugin):
	"""initializes the module and sets up storage methods."""

	def __init__(self) -> None:
		module = sys.modules[__name__]
		module.config = Config()
		module.roles = Roles()
		module.tournament = Tournament()
		print("✅ Initiated storage methods. ")
