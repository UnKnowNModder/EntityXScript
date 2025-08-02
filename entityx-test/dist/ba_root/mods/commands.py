"""commands file."""

from __future__ import annotations
from cmd_core import on_command
from core._enums import Authority, Role, Playlist, Utility
from core._utils import success, send
from core._clients import Client, Player, get_client, get_clients
import core
import bascenev1
import babase


# =================== #
#     USER COMMANDS     #
# =================== #
@on_command(name="/list", aliases=["/ls"])
def list(client: Client):
	"""shows the client, a list of players."""
	clients = get_clients()
	heads = "{0:^16}{1:^14}{2:^12}"
	sep = "\n------------------------------------------------------\n"
	string = heads.format("Name", "Client ID", "Index ID") + sep
	for client in clients:
		string += (
			heads.format(
				client.name, client.client_id, client.index
			)
			+ "\n"
		)
	client.success(string)


@on_command(name="/pb", aliases=["/ac", "/id"])
def show_account_id(client: Client, target: Client):
	"""Shows the client's or target's account ID."""
	target = target or client
	client.send(target.account_id, sender=f"{target.name}'s ID")


@on_command(name="/pm", aliases=["/dm"], usage="/pm <client id> <message>")
def private_message(client: Client, target: Client):
	"""Sends a private message to target client."""
	message = " ".join(args[1:])
	name = f"{client.name} (pvt)"
	target.send(message, sender=name)
	client.send(message, sender=name)


# =================== #
#    ADMIN COMMANDS   #
# =================== #
@on_command(name="/end", aliases=["/over"], authority=Authority.ADMIN)
def end_game(client: Client):
	"""Ends the current game."""
	activity = bascenev1.get_foreground_host_activity()
	with activity.context:
		activity.end_game()
		success(f"{client.name} ended the game")


@on_command(name="/kill", authority=Authority.ADMIN, usage="/kill <index id>")
def kill_player(client: Client, player: Player):
	"""Kill target player"""
	player.kill()


@on_command(name="/freeze", authority=Authority.ADMIN, usage="/freeze <index id>")
def freeze_player(client: Client, player: Player):
	"""Freeze target player"""
	player.freeze()


@on_command(name="/thaw", authority=Authority.ADMIN, usage="/thaw <index id>")
def thaw_player(client: Client, player: Player):
	"""thaw the freezed target player"""
	player.thaw()


@on_command(
	name="/remove",
	aliases=["/rm"],
	authority=Authority.ADMIN,
	usage="/remove <index id>",
)
def remove_player(client: Client, player: Player):
	"""Remove player from game"""
	player.remove()
	client.success(f"Removed {player.name}")


@on_command(
	name="/info",
	aliases=["/gp", "/profiles", "/pf"],
	authority=Authority.ADMIN,
	usage="/info <index id>",
)
def show_profiles(client: Client, player: Player):
	"""Show player profiles"""
	profiles = player.profiles()
	for index, profile in enumerate(profiles, start=1):
		client.send(f"{profile}", sender=f"{index}")


@on_command(name="/say", authority=Authority.ADMIN, usage="/say <message>")
def server_say(client: Client, args: list[str]):
	"""Makes the server say a message."""
	if args[0].startswith("<"):
		# eweheheh some fun.
		client_id = int(args[0].split("<")[1].split(">")[0])
		target = get_client(client_id)
		message = " ".join(args[1:])
		send(message, sender=target.name)
		return
	message = " ".join(args)
	send(message)


@on_command(name="/kick", authority=Authority.ADMIN, usage="/kick <client id>")
def kick_player(client: Client, target: Client):
	"""Kicks a player from the server."""
	if target:
		if target.authority < client.authority:
			target.kick()
			client.success(f"kicked {target.name}")
		else:
			client.error(f"Cannot kick {target.name} (higher authority)")


@on_command(name="/resume", authority=Authority.ADMIN)
def resume_game(client: Client):
	"""Resume paused game"""
	gnode = bascenev1.get_foreground_host_activity().globalsnode
	if gnode.paused:
		gnode.paused = False
		success(f"{client.name} resumed the game")


@on_command(name="/pause", authority=Authority.ADMIN)
def pause_game(client: Client):
	"""Pause current game"""
	gnode = bascenev1.get_foreground_host_activity().globalsnode
	if not gnode.paused:
		gnode.paused = True
		success(f"{client.name} paused the game")


@on_command(name="/restart", aliases=["/quit"], authority=Authority.ADMIN)
def restart_server(client: Client):
	"""Restart server"""
	success(f"{client.name} has hit restart")
	babase.quit()


@on_command(
	name="/max",
	aliases=["/maxplayers", "/mp", "/limit"],
	authority=Authority.ADMIN,
	usage="/max <count>",
)
def set_max_players(client: Client, args: list[str]):
	"""Set max player limit"""
	limit = int(args[0])
	bascenev1.set_public_party_max_size(limit)
	bascenev1.get_foreground_host_session().max_players = limit
	client.success(f"Limit set to {limit}")


@on_command(name="/spectator", aliases=["/lobby"], authority=Authority.ADMIN)
def toggle_spectators(client: Client):
	"""Toggle spectator mode"""
	status = "allowed" if core.config.toggle(Utility.SPECTATOR) else "disallowed"
	success(f"{client.name} has {status} spectators")


@on_command(name="/mute", authority=Authority.ADMIN, usage="/mute <client_id>")
def mute_player(client: Client, target: Client):
	"""Mute player"""
	if target.authority < client.authority:
		if target.mute():
			client.success(f"Muted {target.name}")
			target.error(f"You've been muted by {client.name}")
	else:
		client.error(f"Cannot mute {target.name} (higher authority)")


@on_command(name="/unmute", authority=Authority.ADMIN, usage="/unmute <client_id>")
def unmute_player(client: Client, target: Client):
	"""Unmute player"""
	if target.unmute():
		client.success(f"Unmuted {target.name}")
		target.success(f"You've been unmuted by {client.name}")


@on_command(name="/ffa", authority=Authority.ADMIN)
def set_ffa_playlist(client: Client):
	"""Set FFA playlist"""
	core.config.set_playlist(Playlist.FFA)


@on_command(name="/teams", authority=Authority.ADMIN)
def set_teams_playlist(client: Client):
	"""Set Teams playlist"""
	core.config.set_playlist(Playlist.TEAMS)


# =================== #
#  LEADER COMMANDS   #
# =================== #


@on_command(name="/ban", authority=Authority.LEADER, usage="/ban <account_id>")
def ban_player(client: Client, account_id: str):
	"""Ban player"""
	core.roles.add(Role.BANLIST, account_id)
	client.success(f"Banned {account_id}")


@on_command(name="/unban", authority=Authority.LEADER, usage="/unban <account_id>")
def unban_player(client: Client, account_id: str):
	"""Unban account"""
	core.roles.remove(Role.BANLIST, account_id)
	client.success(f"Unbanned {account_id}")


@on_command(name="/whitelist", aliases=["/wl"], authority=Authority.LEADER)
def toggle_whitelist(client: Client):
	"""Toggle whitelist"""
	status = "enabled" if core.config.toggle(Utility.WHITELIST) else "disabled"
	success(f"{client.name} has {status} whitelist")


@on_command(name="/addwl", authority=Authority.LEADER, usage="/addwl <account_id>")
def add_to_whitelist(client: Client, account_id: str):
	"""Add to whitelist"""
	core.roles.add(Role.WHITELIST, account_id)
	client.success(f"Whitelisted {account_id}")


@on_command(
	name="/removewl",
	aliases=["/rmwl"],
	authority=Authority.LEADER,
	usage="/removewl <account_id>",
)
def remove_from_whitelist(client: Client, account_id: str):
	"""Remove from whitelist"""
	core.roles.remove(Role.WHITELIST, account_id)
	client.success(f"Removed {account_id} from whitelist")


@on_command(name="/admin", authority=Authority.LEADER, usage="/admin <client_id>")
def add_admin(client: Client, target: Client):
	"""Add admin"""
	core.roles.add(Role.ADMIN, target.account_id)
	client.success(f"Added {target.name} as admin")


@on_command(name="/rmadmin", authority=Authority.LEADER, usage="/rmadmin <client_id>")
def remove_admin(client: Client, target: Client):
	"""Remove admin"""
	core.roles.remove(Role.ADMIN, target.account_id)
	client.success(f"Removed {target.name} as admin")
