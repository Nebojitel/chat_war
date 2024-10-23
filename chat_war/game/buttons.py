"""Game buttons and utils."""

import itertools

from telethon import events, types

#Navigate
GO_WEST = '◀️ Go West'
GO_EAST = '▶️️ Go East️'
GO_NORTH = '🔼 Go North'
GO_SOUTH = '🔽️ Go South'
OPEN_MAP = '🗺 Map'

WEST = '◀️'
EAST = '▶️️'
NORTH = '🔼'
SOUTH = '🔽️'
MAP = '🗺'

#Locations
FIELD = '🌻'
FOREST = '🌲'
MOUNTAIN = '🏔'
ME = '📍'
CAMP = '🔥'

#Castles ???
DEERHORN = ''
DRAGONSCALE = ''
HIGHNEST = ''
MOONLIGHT = ''
POTATO = ''
RAMPART = ''
SHARKTEETH = ''
TORTUGA = '🐢'
WOLFPACK = ''

def get_buttons_flat(event: events.NewMessage.Event) -> list[types.TypeKeyboardButton]:
    """Get all available buttons from event message."""
    if not event.message.buttons:
        return []
    return list(itertools.chain(*event.message.buttons))
