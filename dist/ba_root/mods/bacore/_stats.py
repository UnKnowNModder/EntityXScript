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
			self.commit({})
	
	def sort(self) -> dict[str, dict]:
		""" sorts the stats in descending order. """
		stats = self.read()
		sorted_raw = sorted(
			stats.items(),
			key=lambda item: (item[1]["score"], item[1]["kills"], -item[1]["deaths"], item[1]["games"]),
			reverse = True
		)
		sorted_stats = {}
		for rank, (account_id, data) in enumerate(sorted_raw, start=1):
			data = dict(data) # copying to avoid mutating og ref.
			data["rank"] = rank
			sorted_stats[account_id] = data
		self.commit(sorted_stats)