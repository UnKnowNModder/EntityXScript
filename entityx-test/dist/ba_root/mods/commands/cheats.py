""" cheat commands. """
from __future__ import annotations
from . import on_command
from bacore import Authority, Client, Player

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