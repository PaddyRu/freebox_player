# Freebox Player Custom Component for Home Assistant

[![](https://img.shields.io/github/release/PaddyRu/freebox_player/all.svg?style=for-the-badge)](https://github.com/PaddyRu/freebox_player)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![](https://img.shields.io/github/license/PaddyRu/freebox_player?style=for-the-badge)](LICENSE)

This custom component enables remote control on your Freebox Player through both the old and new API.

This component is tested on Freebox Delta, but should also mostly work on Freebox Revolution, Crystal and mini 4K, with a reduced subset however as it doesn't support control through the old remote code API.

This is my first attempt at a HACS (and also Python) project so in the early stages I'll be experiencing with the release process and whatnot so bear with me while I struggle and figure out my way. Thank you for your patience and feedback.
This first implementation takes several shortcuts and only supports controlling fully 1 player, in the future I may heavily change the current code to support a dynamic amount of players based on the data retrieved through the new API.
For now the setup is fairly straightforward.

## Installation

### HACS Install

1. Search for `Freebox Player` under `Integrations` in the HACS Store tab and download it.
3. Add the integration
<a href="https://my.home-assistant.io/redirect/config_flow_start?domain=freebox_player_api" class="my badge" target="_blank"><img src="https://my.home-assistant.io/badges/config_flow_start.svg"></a>

## Features
* On / Off 
* Changing channels
* Volume/Mute/Unmute
* Navigation controls
* Open URL
* Start applications (Netflix, Prime, Apple TV)

## Upcoming features
* Status Retrieval
* Handling of multiple players
* Media Player cards if possible
* ...

## Configuration
Once downloaded, the Freebox Player component needs to be added as in integration from the regular page.

In order to work smoothly you should fix the IP address of your Freebox Player so it doesn't change over time. Then input this IP in the configuration screen, along with the `remote_code` which you can retrieve in different ways depending on the Player you have:
* `Freebox main menu` >> `Parameters` >> `General Information` For old box
* `Freebox main menu` >> `Réglages` >> `Système`>> `Informations Freebox Player et Server` For Delta 

Then upon clicking the "Validate" button you will have to interact with the Freebox Server to grant the integration access to the authenticated API.
Once this is done a final step is needed through the Freebox Server administration website again where you need to navigate to `Paramètres de la Freebox` >> `Mode avancé` >> `Gestion des accès` >> `Applications` and add `Contrôle du Freebox Player` to the list of permissions already granted to the newly registered application. 

## How to use the remote

To send remote code to the player, just call the service `freebox_player_api.remote` with the code in parameter: 
```yaml
code: "power"
```

### Mutiple code

If you want to send multiple code like `123` for example, you need to split each code with a comma :
```yaml
code: "1,2,3"
```

Or you call multiple times the service for each number (`1` && `2` && `3`)

## Button List
### Through the old "remote" API
* "red" // Bouton rouge
* "green" // Bouton vert
* "blue" // Bouton bleu
* "yellow" // Bouton jaune

* "power" // Bouton Power
* "list" // Affichage de la liste des chaines
* "tv" // Bouton tv

* "1" // Bouton 1
* "2" // Bouton 2
* "3" // Bouton 3
* "4" // Bouton 4
* "5" // Bouton 5
* "6" // Bouton 6
* "7" // Bouton 7
* "8" // Bouton 8
* "9" // Bouton 9

* "back" // Bouton jaune (retour)
* "0" // Bouton 0
* "swap" // Bouton swap

* "info" // Bouton info
* "epg" // Bouton epg (fct+)
* "mail" // Bouton mail
* "media" // Bouton media (fct+)
* "help" // Bouton help
* "options" // Bouton options (fct+)
* "pip" // Bouton pip

* "vol_inc" // Bouton volume +
* "vol_dec" // Bouton volume -

* "ok" // Bouton ok
* "up" // Bouton haut
* "right" // Bouton droite
* "down" // Bouton bas
* "left" // Bouton gauche

* "prgm_inc" //Bouton programme +
* "prgm_dec" // Bouton programme -

* "home" // Bouton Free
* "rec" // Bouton Rec

* "prev" // Bouton |<< précédent
* "next" // Bouton >>| suivant

* "tv"
* "replay"
* "vod"
* "whatson"
* "records"
* "media"
* "youtube"
* "radios"
* "canalvod"
* "pip"
* "netflix"

### Through the new authenticated API

* "mute" // Sourdine
* "unmute" // Enlever Sourdine 

* "bwd" // Bouton << retour arrière
* "play_pause" // Bouton Lecture / Pause
* "stop" // Bouton Stop
* "fwd" // Bouton >> avance rapide

* In order to open applications and websites you simply need to put the address starting with https, for instance:
- https://www.primevideo.com
- https://www.netflix.com
- https://www.youtube.com/watch?v=dQw4w9WgXcQ
* The same applies for opening tv channels:
- tv:?channel=2
* And again the same applies for opening VOD services:
- vodservice://replay?currentSelectedService=42 will open mytf1

## Credits
Many thanks to [Pouzor](https://github.com/Pouzor/freebox_player) for his work which pushed me to 