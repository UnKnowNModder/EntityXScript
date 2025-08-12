""" utilities executor plugin. """
# ba_meta require api 9
import babase
from .tournament import replace_old_methods_with_new
from .protector import Protector

# ba_meta export babase.Plugin
class Execute(babase.Plugin):
	def on_app_running(self) -> None:
		""" called on app running. """
		replace_old_methods_with_new()
		Protector().on_app_running()