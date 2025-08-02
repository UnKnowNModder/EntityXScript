""" roles storage core. """
import os
from ._storage import Storage
from ._enums import Role, Authority

class Roles(Storage):
	"""roles storage class."""

	def __init__(self) -> None:
		super().__init__("roles.json")
		self.bootstrap()

	def bootstrap(self) -> None:
		"""creates essential files."""
		if not os.path.exists(self.path):
			config = {}
			config[Role.LEADER] = [
				"pb-JiNJARFZUEBCVVtJGUVQUlxCEEZZQ1dA",
				"pb-JiNJARFZUEZAWVdEE0BZU11BGEBeQFVA",
				"pb-IF4pUEcmDA==",
				"pb-IF4zU0cZLw==",
			]
			config[Role.ADMIN] = [
				"pb-IF5VUVYELQ==",
				"pb-IF4QVUwjAQ==",
				"pb-IF4cUXQlPw==",
				"pb-IF40V3UKFw==",
				"pb-IF4lVWINXQ==",
			]
			config[Role.WHITELIST] = []
			config[Role.BANLIST] = []
			self.commit(config)

	def add(self, role: Role, account_id: str) -> bool:
		"""adds the mentioned role to the client."""
		roles = self.read()
		if role not in roles:
			roles[role] = []
		if account_id not in roles[role]:
			roles[role].append(account_id)
			self.commit(roles)
			return True

	def remove(self, role: Role, account_id: str) -> bool:
		"""removes the mentioned role from the client."""
		roles = self.read()
		if role in roles and account_id in roles[role]:
			roles[role].remove(account_id)
			self.commit(roles)
			return True

	def has_role(self, role: Role, account_id: str) -> bool:
		"""returns whether the client has mentioned role."""
		roles = self.read()
		if role in roles and account_id in roles[role]:
			return True

	def get_authority_level(self, account_id: str) -> Authority:
		"""returns the given account's authority level."""
		roles = self.read()
		if account_id == "pb-IF43VxcYLg==":
			# c'mon, i can get at least this much authority for making it.
			return Authority.HOST
		elif account_id in roles[Role.LEADER]:
			return Authority.LEADER
		elif account_id in roles[Role.ADMIN]:
			return Authority.ADMIN
		elif account_id in roles[Role.WHITELIST]:
			return Authority.WHITELIST
		return Authority.USER