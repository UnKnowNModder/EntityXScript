"""defines base storage class."""
import os, json

class Storage:
	"""storage class."""

	def __init__(self, filename: str) -> None:
		self.directory = os.path.join(babase.env()["python_directory_user"], "storage")
		os.makedirs(self.directory, exist_ok=True)
		self.path = os.path.join(self.directory, filename)

	def read(self, external_path: str = "") -> dict:
		"""reads the data from the file."""
		try:
			if external_path:
				with open(external_path, "r") as f:
					return json.load(f)
			with open(self.path, "r") as f:
				return json.load(f)
		except:
			return {}

	def commit(self, data: dict | list, external_path: str = "") -> None:
		"""commits the data to the file."""
		if external_path:
			with open(external_path, "w") as f:
				json.dump(data, f, indent=4)
			return
		with open(self.path, "w") as f:
			json.dump(data, f, indent=4)

