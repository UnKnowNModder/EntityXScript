"""core file that binds everything."""

# ba_meta require api 9
import bascenev1, babase
from storage import Storage, Config, Roles, Tournament
from protector import Protector
from tournament import replace


# ba_meta export babase.Plugin
class Initialize(babase.Plugin):
    """initializes the module and sets up methods."""

    def __init__(self) -> None:
        bascenev1.storage = Storage()
        bascenev1.storage.config = Config()
        bascenev1.storage.roles = Roles()
        bascenev1.storage.tournament = Tournament()
        print("✅ Initiated storage methods. ")
        self.protector = Protector()
        replace()
        print("✅ Initiated tournament utility. ")

    def on_app_running(self) -> None:
        self.protector.on_app_running()
