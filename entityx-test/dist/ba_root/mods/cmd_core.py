"""core command file."""

# thanks to snoweee for enlightening me with decorators <3
from __future__ import annotations
from clients import Client, get_client, get_player
from enums import Authority

_commands = {}


def on_command(
	name: str,
	aliases: list[str] = [],
	authority: Authority = Authority.USER,
	usage: str = "",
):
	"""decorator to register a command."""

	def decorator(function):
		cmd = {"call": function, "authority": authority, "usage": usage}
		_commands[name] = cmd
		if aliases:
			for aliase in aliases:
				_commands[aliase] = cmd
		return function

	return decorator


def command_line(msg: str, client: Client) -> str | None:
	"""processes a chat message as a command.
	AKA command line as the name says."""
	command = msg.split()[0].lower()
	args = msg.split()[1:]
	if command in _commands:
		cmd = _commands[command]
		if client.authority >= cmd["authority"]:
			function = cmd["call"]
			params = function.__code__.co_varnames
			try:
				if "args" in params:
					function(client, args)
				elif "target" in params:
					target = get_client(args[0])
					function(client, target)
				elif "player" in params:
					player = get_player(args[0])
					function(client, player)
				elif "account_id" in params:
					function(client, args[0])
				else:
					function(client)
			except:
				client.error(f"Usage: {cmd['usage']}")
			return
	# wasn't any command.
	return msg
