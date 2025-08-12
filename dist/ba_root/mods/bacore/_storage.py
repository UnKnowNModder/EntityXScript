"""defines base storage class."""
from __future__ import annotations
from pathlib import Path
from typing import Optional
import json, babase

class Storage:
	"""storage class."""

	def __init__(self, filename: str) -> None:
		self.directory = Path(babase.env()["python_directory_user"]) / "storage"
		self.directory.mkdir(parents=True, exist_ok=True)
		self.path = self.directory / filename

	def read(self, external_path: Optional[Path] = None) -> dict:
		"""reads the data from the file."""
		target_path = external_path or self.path
		try:
			with target_path.open("r") as f:
				return json.load(f)
		except (FileNotFoundError, json.JSONDecodeError):
			return {}

	def commit(self, data: dict | list, external_path: Optional[Path] = None) -> None:
		"""commits the data to the file."""
		target_path = external_path or self.path
		with target_path.open("w") as f:
			json.dump(data, f, indent=4)

