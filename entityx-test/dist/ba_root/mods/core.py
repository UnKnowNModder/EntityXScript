"""core file that binds everything."""

# ba_meta require api 9
import babase, sys
from storage import Storage, Config, Roles, Tournament
from protector import Protector
from tournament import replace_old_methods_with_new


# ba_meta export babase.Plugin
class Initialize(babase.Plugin):
	"""initializes the module and sets up methods."""

	def __init__(self) -> None:
		module = sys.modules(__name__)
		module.storage = Storage()
		module.storage.config = Config()
		module.storage.roles = Roles()
		module.storage.tournament = Tournament()
		print("✅ Initiated storage methods. ")
		replace_old_methods_with_new()
		print("✅ Initiated tournament utility. ")

	def on_app_running(self) -> None:
		Protector().on_app_running()
