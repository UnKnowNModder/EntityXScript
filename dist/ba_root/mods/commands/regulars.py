"""regular commands."""

from __future__ import annotations

import bascenev1

from server.clients import Client, all_clients

from . import on_command


@on_command(name="/list", aliases=["/ls"])
def list(client: Client):
    """shows the client, a list of players."""
    heads = "{0:^16}{1:^15}{2:^15}\n"
    sep = "--------------------------------------------------------------\n"
    string = heads.format("Name", "Client ID", "Index ID") + sep
    if session := bascenev1.get_foreground_host_session():
        for index, player in enumerate(session.sessionplayers):
            string += heads.format(
                player.getname(True, True), player.inputdevice.client_id, index
            )
    for i in bascenev1.get_game_roster()[1:]:
        if str(i["client_id"]) not in string:
            string += heads.format(i["display_string"], i["client_id"], "<in lobby>")
    client.success(string)


@on_command(name="/stats")
def show_stats(client: Client) -> None:
    """shows the client his stats."""
    from stats import stats

    if _stats := stats.get(client.account_id):
        message = "{} | score: {} | kills: {} | deaths: {} | games: {}".format(
            _stats["rank"],
            _stats["score"],
            _stats["kills"],
            _stats["deaths"],
            _stats["games"],
        )
        client.send(message, sender="rank")
        return
    client.error("Your stats will be available soon.")


@on_command(name="/pb", aliases=["/ac", "/id"])
def show_account_id(client: Client, target: Client):
    """Shows the client's or target's account ID."""
    target = target or client
    client.send(target.account_id, sender=f"{target.name}'s ID")


@on_command(name="/pm", aliases=["/dm"], usage="/pm <client id> <message>")
def private_message(client: Client, target: Client, message: str):
    """Sends a private message to target client."""
    name = f"{client.name} (pvt)"
    target.send(message, sender=name)
    client.send(message, sender=name)


@on_command(name="/ping", aliases=["/ms"])
def show_ping(client: Client):
    """shows the client's ping"""
    message = f"Your ping: {client.ping} ms"
    client.send(message)


@on_command(name="/pingall", aliases=["/msall"])
def show_all_pings(client: Client):
    """shows all the connected clients' ping"""
    text_format = "{}'s ping: {} ms"
    for _client in all_clients():
        client.send(text_format.format(_client.name, _client.ping))

@on_command(name="/character", aliases=["/char", "/c"], usage="/character list (to see index of available characters) or /character <index>)")
def character(client: Client, args: list[str]):
    """ changes the character to the one specified."""
    characters = [
        "Spaz",
        "Zoe",
        "Snake Shadow",
        "Kronk",
        "Mel",
        "Jack Morgan",
        "Santa Claus",
        "Frosty",
        "Bones",
        "Bernard",
        "Pascal",
        "Taobao Mascot",
        "B-9000",
        "Agent Johnson",
        "Grumbledorf",
        "Pixel",
        "Easter Bunny",
    ]
    if args[0].lower() in ["l", "list"]:
        for index, char in enumerate(characters):
            client.send(f"{index+1}: {char}")
        client.send("Type /character <index> to change your character.")
        return

    new_character = characters[int(args[0])-1]
    sessionplayers = bascenev1.get_foreground_host_session().sessionplayers
    for player in sessionplayers:
        if player.inputdevice.client_id == client.client_id:
            # set in session (for as long as the session goes on.)
            player.setdata(player.sessionteam, new_character, player.color, player.highlight)
            # set in activity (for as long as this gameactivity is active, this makes sure the character is changed even after respawn.)
            player.activityplayer.character = new_character
            # set in player spaz node for instant change.
            with bascenev1.get_foreground_host_activity().context:
                appearances = bascenev1.app.classic.spaz_appearances
                appearance = appearances[new_character]
                activityplayer = player.activityplayer
                node = activityplayer.actor.node
                node.color_texture = bascenev1.gettexture(appearance.color_texture)
                node.color_mask_texture = bascenev1.gettexture(appearance.color_mask_texture)
                node.head_mesh = bascenev1.getmesh(appearance.head_mesh)
                node.torso_mesh = bascenev1.getmesh(appearance.torso_mesh)
                node.pelvis_mesh = bascenev1.getmesh(appearance.pelvis_mesh)
                node.upper_arm_mesh = bascenev1.getmesh(appearance.upper_arm_mesh)
                node.forearm_mesh = bascenev1.getmesh(appearance.forearm_mesh)
                node.hand_mesh = bascenev1.getmesh(appearance.hand_mesh)
                node.upper_leg_mesh = bascenev1.getmesh(appearance.upper_leg_mesh)
                node.lower_leg_mesh = bascenev1.getmesh(appearance.lower_leg_mesh)
                node.toes_mesh = bascenev1.getmesh(appearance.toes_mesh)
                node.style = appearance.style

                player.set_icon_info(appearance.icon_texture, appearance.icon_mask_texture, player.color, player.highlight)
                if hasattr(player.activityplayer, "icons") and player.activityplayer.icons:
                    player.activityplayer.icons[0].node.texture = bascenev1.gettexture(appearance.icon_texture) 
                    player.activityplayer.icons[0].node.tint_texture = bascenev1.gettexture(appearance.icon_mask_texture)
                client.success(f"Changed character to {new_character}")
                break
