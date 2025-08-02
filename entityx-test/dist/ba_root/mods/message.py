"""handles control over messages."""

from __future__ import annotations
from clients import Dummy, get_client
import cmd_core as core
import commands


def filter_chat_message(msg: str, client_id: int):
    client = Dummy(client_id, "Host") if client_id == -1 else get_client(client_id)
    if not client:
        return
    if client.is_mute:
        print(f"{client.name} (muted): {msg}")
        return
    return core.command_line(msg, client)
