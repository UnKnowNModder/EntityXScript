""" utilities loader plugin. """
# ba_meta require api 9
import babase, bacore
from .bot import start_bot_utility
from .protector import Protector

def _load_utilities():
    """automatically imports utility files in the directory."""
    package_dir = Path(__file__).parent
    for file in package_dir.glob("*.py"):
        if file.stem == "__init__" or file.stem == "bot":
            continue
        module_name = f"{__package__}.{file.stem}"
        try:
            importlib.import_module(module_name)
            print(f"✅ Loaded {file.stem} utility.")
        except ImportError:
            print(f"⚠️ Failed to load command file {file.stem}")

# ba_meta export babase.Plugin
class Execute(babase.Plugin):
	def on_app_running(self) -> None:
		""" called on app running. """
		Protector()
		if bacore.config.read()["bot"]:
			start_bot_utility()
		_load_utilities()