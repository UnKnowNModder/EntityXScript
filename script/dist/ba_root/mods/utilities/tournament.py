"""tournament related."""

from __future__ import annotations
from commands import on_command
from bacore import Dummy, Client, Authority
import bacore, bascenev1, babase
import baclassic._servermode
import bascenev1lib.activity.multiteamvictory

series: list = []  # i like lists.. (more like i hate using global keyword)


def new_handle_transition(self) -> bool:
	# this is a modified function of ServerController class..
	if bacore.tournament.match:
		# we don't wanna restart yet if a match is ongoing/registered.
		return False
	if self._shutdown_reason is not None:
		self._execute_shutdown()
		return True
	return False


old_on_begin = (
	bascenev1lib.activity.multiteamvictory.TeamSeriesVictoryScoreScreenActivity.on_begin
)


def new_on_begin(self) -> None:
	if match := bacore.tournament.match:
		# a series has ended-.
		series.append(
			1
		)  # whatever value is fine, we js want the length to increase by 1.
		if len(series) == match["series"]:
			# hmph, the given series count has matched.
			series.clear()
			# save the result
			bacore.tournament.save_result(self.settings_raw["winner"])
		else:
			bacore.success(f"Series: {len(series)}/{match['series']}")
	old_on_begin(self)


old_on_player_request = bascenev1._session.Session.on_player_request


def new_on_player_request(self, player: bascenev1.SessionPlayer) -> bool:
	client = Dummy(player.inputdevice.client_id, player.get_v1_account_id())
	if not client.authenticity:
		auth_code = client.get_auth_code()
		client.error(f"Your auth code is: {auth_code}\nPlease enter in chat to verify.")
		return False
	if match := bacore.tournament.match:
		if client.account_id not in match["players"]:
			# match is on.
			client.error("You cannot join in between matches.. ")
			return False
	result = old_on_player_request(self, player)
	return result


old_on_team_join = bascenev1._dualteamsession.DualTeamSession.on_team_join


def new_on_team_join(self, team: bascenev1.SessionTeam) -> None:
	old_on_team_join(self, team)
	if match := bacore.tournament.match:
		account_id = team.players[0].get_v1_account_id()
		team1_name, members1 = next(iter(match["team1"].items()))
		if account_id in members1:
			team.name = team1_name
			return
		team2_name, members2 = next(iter(match["team2"].items()))
		if account_id in members2:
			team.name = team2_name
			return


## tournament-related commands.


@on_command(name="/confirm")
def confirm(client: Client) -> None:
	"""confirms the client to the tournament match."""
	if status := bacore.tournament.confirm(client.account_id):
		client.success("You've been confirmed in the match. ")
		return
	client.error("You're not in any match, cannot confirm.")


@on_command(
	name="/discard", aliases=["/endmatch", "/rmmatch"], authority=Authority.LEADER
)
def discard(client: Client):
	"""discards the match if registered..
	it can be up again if players confirm."""
	if match := bacore.tournament.match:
		match.clear()
		series.clear()
		client.success("Match has been discarded.")
		return
	client.error("No match is registered. ")


def replace_old_methods_with_new() -> None:
	"""replaces the original methods with newly defined ones."""
	bascenev1._session.Session.on_player_request = new_on_player_request
	baclassic._servermode.ServerController.handle_transition = new_handle_transition
	bascenev1lib.activity.multiteamvictory.TeamSeriesVictoryScoreScreenActivity.on_begin = new_on_begin
	bascenev1._dualteamsession.DualTeamSession.on_team_join = new_on_team_join
	print("✅ Executed tournament utility. ")
