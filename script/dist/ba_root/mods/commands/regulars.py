""" regular commands. """
from __future__ import annotations
from . import on_command
from bacore import Client, all_clients

@on_command(name="/list", aliases=["/ls"])
def list(client: Client):
	"""shows the client, a list of players."""
	clients = all_clients()
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