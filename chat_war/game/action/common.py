"""Common game actions."""
import logging
import random

from telethon import events

from chat_war.settings import app_settings
from chat_war.telegram_client import client
from chat_war.wait_utils import wait_for
from chat_war.game.buttons import GO_WEST, GO_EAST, GO_NORTH, GO_SOUTH, OPEN_MAP

BAG = '/bag'
STOCK = '/stock'

NEXT = '/next'
TOUR = '/tour'

HERO = '/hero'
LEVEL_UP = '/level_up'
UP_STR = '/up_str'
UP_DEX = '/up_dex'
UP_VIT = '/up_vit'

async def ping(entity: int | events.NewMessage.Event) -> None:
    """Random short message for update current location state."""
    logging.info('call ping command')

    if isinstance(entity, events.NewMessage.Event):
        game_bot_id = entity.chat_id
    else:
        game_bot_id = entity

    message = random.choice(
        seq=app_settings.ping_commands,
    )
    logging.info(f'call ping command debug {game_bot_id} {message}')
    await wait_for()
    await client.send_message(
        entity=game_bot_id,
        message=message,
    )

async def execute_command(entity: int, command: str) -> None:
    """Execute custom command."""
    logging.info('call command execution {0}'.format(command))
    await wait_for()
    await client.send_message(
        entity=entity,
        message=command,
    )

async def show_hero(entity: int | events.NewMessage.Event) -> None:
    """Call show hero info."""
    logging.info('call show hero info command')

    if isinstance(entity, events.NewMessage.Event):
        game_bot_id = entity.chat_id
    else:
        game_bot_id = entity

    await execute_command(
        entity=game_bot_id,
        command=HERO,
    )

async def show_map(event: events.NewMessage.Event) -> None:
    """Call show map."""
    logging.info('call show map button')
    await wait_for()
    await client.send_message(
        entity=event.chat_id,
        message=OPEN_MAP,
    )

async def go_north(event: events.NewMessage.Event) -> None:
    """Call go north."""
    logging.info('call go north button')
    await wait_for()
    await client.send_message(
        entity=event.chat_id,
        message=GO_NORTH,
    )

async def go_south(event: events.NewMessage.Event) -> None:
    """Call go south."""
    logging.info('call go south button')
    await wait_for()
    await client.send_message(
        entity=event.chat_id,
        message=GO_SOUTH,
    )

async def go_east(event: events.NewMessage.Event) -> None:
    """Call go east."""
    logging.info('call go east button')
    await wait_for()
    await client.send_message(
        entity=event.chat_id,
        message=GO_EAST,
    )

async def go_west(event: events.NewMessage.Event) -> None:
    """Call go west."""
    logging.info('call go west button')
    await wait_for()
    await client.send_message(
        entity=event.chat_id,
        message=GO_WEST,
    )
