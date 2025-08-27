""" tournament storage core. """
from __future__ import annotations
import os
import babase, bascenev1
from ._storage import Storage
from ._clients import Client
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
		match["confirmed"] = []
		tournament.append(match)
		self.commit(tournament)

	def discard(self, id: int) -> None:
		"""discards a match."""
		tournament = self.read()
		tournament = [match for match in tournament if match["id"] != id]
		self.commit(tournament)

	def register(self, match_id: int, team_name: str, account_id: str) -> str:
		""" register a player in a tournament match. """
		tournament = self.read()
		for match in tournament:
			if match["id"] != match_id:
				continue
			for team in match["teams"]:
				if team["name"] != team_name:
					continue
				if account_id not in team["participants"]:
					team["participants"].append(account_id)
					self.commit(tournament)
					return "You have been registered in Team {}.".format(team_name)
				else:
					return "You are already registered in Team {}.".format(team_name)
			return "No team found with the provided name."
		return "No match found with the provided id."

	def get_player_team(self, player: bascenev1.SessionPlayer) -> dict:
		""" returns the tournament team this player is associated with. """
		account_id = player.get_v1_account_id()
		for team in self.match["teams"]:
			if account_id in team["participants"]:
				return team
		return {}


	def confirm(self, client: Client) -> bool | None:
		"""confirms the client if they are in a match."""
		# check: if any match is ongoing
		if self.match:
			client.error("A match is in progress — confirmation unavailable.")
			return False
		account_id = client.account_id
		tournament = self.read()
		for match in tournament:
			all_members = match["teams"][0]["participants"] + match["teams"][1]["participants"]

			if account_id in all_members:
				if account_id in match["confirmed"]:
					# ah, double confirm, pretty smart huh?
					client.error("You have already confirmed.")
					return False
				match["confirmed"].append(account_id)
				if len(match["confirmed"]) == len(all_members):
					# all clients have been registered, assign the self.match it's value.
					self.match = match
					# load and start the tournament session.
					with babase.ContextRef.empty():
						babase.apptimer(2.0, self.begin)
					# clean up.
					tournament.remove(match)
				self.commit(tournament)
				client.success("You have been successfully confirmed.")
				return True
		client.error("You are not part of any match.")

	def declare(self, winner: bascenev1.SessionTeam, message: str) -> None:
		"""declares a match winner and saves it."""
		success(message)
		self.discard(self.match["id"])
		self.match["winner"] = winner.name
		results = self.read(self.results)
		results.append(self.match)
		self.commit(results, self.results)
		babase.app.classic.server._execute_shutdown()
		

	def begin(self) -> None:
		"""begins the tournament session."""
		# start the match.
		from utilities import TournamentSession
		call = babase.Call(bascenev1.new_host_session, TournamentSession)
		babase.pushcall(call)
		success("Your match is about to begin.")