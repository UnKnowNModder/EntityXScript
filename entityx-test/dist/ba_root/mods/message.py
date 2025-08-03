"""handles control over messages."""

from __future__ import annotations
from bacore import Dummy, fetch_client
import commands

def filter_chat_message(msg: str, client_id: int):
	client = Dummy(client_id, "Host") if client_id == -1 else fetch_client(client_id)
	if not client or not msg:
		return
	if not client.authenticity:
		auth_code = client.get_auth_code()
		if not client.verify_auth_code(msg.split()[0]):
			client.error(f"Your auth code is: {auth_code}\nPlease enter in chat to verify.")
		return
	if client.is_mute:
		print(f"{client.name} (muted): {msg}")
		return
	return commands.command_line(msg, client)
