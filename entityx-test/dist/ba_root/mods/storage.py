"""storage that holds file configuration."""

from enums import Role, Utility, Authority, Playlist, Match
from typing import override
from clients import Client
import bascenev1, babase
import os, json
from utils import success


class Storage:
    """storage class."""

    def __init__(self) -> None:
        self.directory = os.path.join(babase.env()["python_directory_user"], "storage")
        os.makedirs(self.directory, exist_ok=True)

    def read(self) -> dict:
        """reads the data from the file."""
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except:
            return {}

    def commit(self, data: dict | list) -> None:
        """commits the data to the file."""
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)


class Config(Storage):
    """config storage class."""

    def __init__(self) -> None:
        super().__init__()
        self.path = os.path.join(self.directory, "config.json")
        self.toml = os.path.join(
            f"{os.sep}".join(os.getcwd().split(os.sep)[:-1]), "config.toml"
        )
        self.bootstrap()

    def bootstrap(self) -> None:
        """creates essential files."""
        if not os.path.exists(self.path):
            config = {}
            config[Utility.WHITELIST] = False
            config[Utility.SPECTATOR] = True
            self.commit(config)

    def toggle(self, utility: Utility) -> bool:
        """toggles the utility."""
        config = self.read()
        if not utility in config:
            config[utility] = True
        config[utility] = not config[utility]
        self.commit(config)
        return config[utility]

    def set_playlist(self, playlist: Playlist) -> None:
        """changes the playlist code in .toml file."""
        code = playlist.value
        with open(self.toml, "r") as f:
            lines = f.readlines()
        with open(self.toml, "w") as f:
            for line in lines:
                if line.strip().startswith(f"playlist_code ="):
                    f.write(f"playlist_code = {code}\n")
                else:
                    f.write(line)

    @property
    def whitelist(self) -> bool:
        """returns whether whitelist is enable or not."""
        config = self.read()
        if Utility.WHITELIST not in config:
            config[Utility.WHITELIST] = False
        return config[Utility.WHITELIST]

    @property
    def spectator(self) -> bool:
        """returns whether spectator is enable or not."""
        config = self.read()
        if Utility.SPECTATOR not in config:
            config[Utility.SPECTATOR] = True
        return config[Utility.SPECTATOR]


class Roles(Storage):
    """roles storage class."""

    def __init__(self) -> None:
        super().__init__()
        self.path = os.path.join(self.directory, "roles.json")
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


class Tournament(Storage):
    """tournament storage class."""

    def __init__(self) -> None:
        super().__init__()
        self.path = os.path.join(self.directory, "tournament.json")
        self.results = os.path.join(self.directory, "tournament_results.json")
        self.match: Match = {}
        self.bootstrap()

    @override
    def read(self, path: str = None) -> dict:
        """reads the data from the file."""
        try:
            if path:
                with open(path, "r") as f:
                    return json.load(f)
            with open(self.path, "r") as f:
                return json.load(f)
        except:
            return {}

    @override
    def commit(self, data: dict | list, path: str = None) -> None:
        """commits the data to the file."""
        if path:
            with open(path, "w") as f:
                json.dump(data, f, indent=4)
            return
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

    def bootstrap(self) -> None:
        """creates tournament file."""
        if not os.path.exists(self.path):
            self.commit([])
        if not os.path.exists(self.results):
            self.commit([], self.results)

    def insert(self, match: Match) -> None:
        """inserts the match to the database."""
        tournament = self.read()
        match["id"] = len(tournament) + 1
        match["players"] = []
        tournament.append(match)
        self.commit(tournament)

    def discard(self, id: int) -> None:
        """discards the match with it's id."""
        tournament = self.read()
        tournament = [match for match in tournament if match["id"] != id]
        self.commit(tournament)

    def confirm(self, client: str) -> bool:
        """confirms the client if they are in a match."""
        tournament = self.read()
        for index, match in enumerate(tournament):
            all_members = (
                list(match["team1"].values())[0] + list(match["team2"].values())[0]
            )  # messy but works.

            if client in all_members:
                match["players"].append(client)
                tournament[index] = match
                if len(match["players"]) == len(all_members):
                    # all clients have been registered, assign the self.match it's value.
                    self.match = match
                    # do registeration.
                    self.on_match_registration()
                    # clean up.
                    tournament.remove(match)
                self.commit(tournament)
                return True

    def save_result(self, winner: bascenev1.SessionTeam) -> None:
        """registers a match result."""
        id = self.match["id"]
        self.discard(id)
        results = self.read(self.results)
        results.append({"id": id, "winner": str(winner.name)})
        self.commit(results, self.results)
        with bascenev1.get_foreground_host_session().context:
            success("The server will restart soon. ")
            bascenev1.timer(5, babase.quit)

    def on_match_registration(self) -> None:
        """called when a match has been registered."""

        # start the match.
        def start_over():
            babase.pushcall(
                bascenev1.Call(
                    bascenev1.new_host_session,
                    bascenev1._dualteamsession.DualTeamSession,
                )
            )

        with bascenev1.get_foreground_host_session().context:
            bascenev1.timer(2, start_over)
            success("Match is starting soon.. be ready..")
