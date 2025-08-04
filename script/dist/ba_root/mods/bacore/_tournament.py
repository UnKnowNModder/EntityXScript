""" tournament storage core. """
from __future__ import annotations
import os
import babase, bascenev1
from ._storage import Storage
from ._enums import Match
from ._utils import success

class Tournament(Storage):
	"""tournament storage class."""

	def __init__(self) -> None:
		super().__init__("tournament.json")
		self.results = self.directory / "tournament_results.json"
		self.match: Match = {}
		self.bootstrap()

	def bootstrap(self) -> None:
		"""creates tournament file."""
		if not self.path.exists():
			self.commit([])
		if not self.results.exists():
			self.commit([], self.results)

	def insert(self, match: Match) -> None:
		"""inserts the match to the database."""
		tournament = self.read()
		match["id"] = len(tournament) + 1
		match["players"] = []
		tournament.append(match)
		self.commit(tournament)

	def discard(self, id: int) -> None:
		"""discards the match with it's id."""
		tournament = self.read()
		tournament = [match for match in tournament if match["id"] != id]
		self.commit(tournament)

	def confirm(self, client: str) -> bool:
		"""confirms the client if they are in a match."""
		tournament = self.read()
		for index, match in enumerate(tournament):
			all_members = (
				list(match["team1"].values())[0] + list(match["team2"].values())[0]
			)  # messy but works.

			if client in all_members:
				match["players"].append(client)
				tournament[index] = match
				if len(match["players"]) == len(all_members):
					# all clients have been registered, assign the self.match it's value.
					self.match = match
					# do registeration.
					self.on_match_registration()
					# clean up.
					tournament.remove(match)
				self.commit(tournament)
				return True

	def save_result(self, winner: bascenev1.SessionTeam) -> None:
		"""registers a match result."""
		id = self.match["id"]
		self.discard(id)
		results = self.read(self.results)
		results.append({"id": id, "winner": str(winner.name)})
		self.commit(results, self.results)
		with bascenev1.get_foreground_host_session().context:
			success("The tournament match has ended..\nThe server will restart soon. ")
			bascenev1.timer(5, babase.quit)

	def on_match_registration(self) -> None:
		"""called when a match has been registered."""

		# start the match.
		def start_over():
			babase.pushcall(
				bascenev1.Call(
					bascenev1.new_host_session,
					bascenev1._dualteamsession.DualTeamSession,
				)
			)

		with bascenev1.get_foreground_host_session().context:
			bascenev1.timer(2, start_over)
			success("Match is starting soon.. be ready..")