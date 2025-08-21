""" stats storage core. """
from __future__ import annotations
from ._storage import Storage

class Stats(Storage):
	"""stats storage class."""

	def __init__(self) -> None:
		super().__init__("stats.json")
		self.bootstrap()

	def bootstrap(self) -> None:
		"""creates essential files."""
		if not self.path.exists():
			self.commit([])
	
	def get(self) -> list[dict]:
		""" returns sorted stats. """
		