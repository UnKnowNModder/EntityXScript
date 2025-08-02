"""types file for storage."""

from enum import IntEnum, StrEnum
from typing import TypedDict, NotRequired


class Authority(IntEnum):
	"""enum class for authority levels."""

	USER = 0
	WHITELIST = 1
	ADMIN = 2
	LEADER = 3
	HOST = 10  # for server.


class Role(StrEnum):
	"""enum class for roles."""

	LEADER = "leaders"
	ADMIN = "admins"
	WHITELIST = "whitelist"
	BANLIST = "banlist"


class Utility(StrEnum):
	"""enum class for utilities."""

	WHITELIST = "whitelist"
	SPECTATOR = "spectator"


class Playlist(IntEnum):
	"""enum class for playlists."""

	TEAMS = 531064
	FFA = 531063


class Match(TypedDict):
	"""match type."""

	id: NotRequired[int]
	series: int
	team1: dict[str, list[str]]
	team2: dict[str, list[str]]
	players: NotRequired[list[str]]
