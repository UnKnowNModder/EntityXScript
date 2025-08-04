# Bombsquad Server Scripts
it's a modified version server scripts
it has a few features and utilities described below.
- script version: 1.7.46 (dev)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## Features:
- has important commands
- tournament utility
- protection (v2 check)
- party and session leave/join messages has been removed
- once a week OTP verification for every player.

## Tournament Utility:
- it's basically an utility that manages tournament matches, the methods for it can be seen in bacore/_tournament.py, it's not much advanced but helpful.
- the matches should be added through discord bot / through manual code (the support for in-game commands has not been added)
- /confirm command for participents who have been registered in a match, once all participents of a specific match has been confirmed, the match will automatically start
- after the match ends, the result will be stored in tournament_results.json, along with the winner team's name.


# Todo:
- add support for discord bot
- add team lives balancer
- todo: add more TODOs :D


## Modification?
- yup, you can modify it and use however you want in your scripts.
- whether you need to take a bit of idea to copy paste some code, you can do it all.
- (credit isn't needed just so you know)