# Ballistica server scripts.
it's a modified version of the vanilla,
it has a few features and utilities described below.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## Current Features:
- has important commands
- tournament utility
- protection (v2 check)
- party and session leave/join messages has been removed
- a devicename.txt will be created in your dist alongside headless binary, you can change your server's device name in that.

## Tournament Utility:
- it's basically an utility that manages tournament matches, the storage for it can be seen in storage.py, it's not much advanced but helpful.
- the matches should be added through discord bot / through manual code (the support for in-game commands has not been added)
- /confirm command for participents who have been registered in a match, once all participents of a specific match has been confirmed, the match will automatically start
- after the match ends, the result will be stored in tournament_results.json, along with the winner team's name.


# Todo:
- fix formats of storage
- add support for discord bot
- create a seperate Target class for commands
- create an own package and attach it storage methods instead of bascenev1
- add team lives balancer
- todo: add more TODOs :D


## Discord Bot:
- the discord bot should directly use bascenev1.storage class (look at storage.py for available methods.)
- create an schedule match command to add matches to database (dict type should be Match as defined in types.go)
- mostly in-game commands would be handled through bascenev1.chatmessage
- more-coming...

## Modification?
- yup, you can modify it and use however you want in your scripts.
- whether you need to take a bit of idea to copy paste some code, you can do it all.
- (credit isn't needed just so you know)
