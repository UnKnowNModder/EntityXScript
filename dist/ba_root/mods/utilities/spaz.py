""" modified spaz functionality. """
from __future__ import annotations
from typing import Sequence
import bascenev1 as bs
import bacore
from bascenev1lib.actor import playerspaz

class Text:
	""" text which spawns on the node's head. """
	def __init__(self, node: bs.Node, text: str) -> None:
		color = (1, 1, 1) # default
		self.node = node
		math = bs.newnode(
			"math", 
			owner = self.node,
			attrs = {
				"input1": (0, 1.3, 0),
				"operation": "add"
			}
		)
		self.node.connectattr("torso_position", math, "input2")
		
		self.text = bs.newnode(
			"text",
			owner = self.node,
			attrs = {
				"text": text,
				"in_world": True,
				"shadow": 1.1,
				"flatness": 1.0,
				"color": color,
				"scale": 0.01,
				"h_align": "center"
			}
		)
		math.connectattr("output", self.text, "position")
		# bs.animate_array(self.text, "scale", {0: 0.0, 1: 0.01})
		
def attach_rank(self, player: bs.Player) -> None:
	""" attaches the rank on player head. """
	if player and player.sessionplayer:
		account_id = player.sessionplayer.get_v1_account_id()
		stats = bacore.stats.get(account_id)
		if stats:
			rank = f"#{stats['rank']}"
			Text(self.node, rank)

old_init = playerspaz.PlayerSpaz.__init__

def new_init(self,player: bs.Player,*,color: Sequence[float] = (1.0, 1.0, 1.0),highlight: Sequence[float] = (0.5, 0.5, 0.5),character: str = "Spaz",powerups_expire: bool = True):
	""" modified constructor of PlayerSpaz class. """
	old_init(self,player=player,color=color,highlight=highlight,character=character,powerups_expire=powerups_expire)
	attach_rank(self, player)

def patch() -> None:
	""" patches the modified spaz to original one. """
	playerspaz.PlayerSpaz.__init__ = new_init