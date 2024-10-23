import logging
from typing import Callable

from telethon import events, types

from chat_war import stats
from chat_war.game import action, state
from chat_war.plugins import manager
from chat_war.settings import app_settings, game_bot_name
from chat_war.telegram_client import client
from chat_war.trainer import event_logging, loop
from chat_war.trainer.handlers import common, farming


async def main(execution_limit_minutes: int | None = None) -> None:
    """Farming runner."""
    local_settings = {
        'execution_limit_minutes': execution_limit_minutes or 'infinite',
        'notifications_enabled': app_settings.notifications_enabled,
        'slow_mode': app_settings.slow_mode,
    }
    logging.info(f'start farming ({local_settings})')

    logging.info('auth as %s', (await client.get_me()).username)

    game_user: types.InputPeerUser = await client.get_input_entity(game_bot_name)
    logging.info('game user is %s', game_user)

    await client.send_message(game_bot_name, action.common_actions.HERO)

    await _setup_handlers(game_user_id=game_user.user_id)

    await loop.run_wait_loop(execution_limit_minutes)
    logging.info('end farming')


async def _setup_handlers(game_user_id: int) -> None:
    if app_settings.self_manager_enabled:
        manager.setup(client)

    client.add_event_handler(
        callback=_message_handler,
        event=events.NewMessage(
            incoming=True,
            from_users=(game_user_id,),
        ),
    )
    client.add_event_handler(
        callback=_message_handler,
        event=events.MessageEdited(
            incoming=True,
            from_users=(game_user_id,),
        ),
    )


async def _message_handler(event: events.NewMessage.Event) -> None:
    await event_logging.log_event_information(event)
    stats.collector.inc_value('events')

    await event.message.mark_read()

    select_callback = _select_action_by_event(event)

    await select_callback(event)


def _select_action_by_event(event: events.NewMessage.Event) -> Callable:
    mapping = [
        (state.common_states.is_hero_state, farming.processing),
        (state.common_states.is_empty_energy, farming.relaxing),
    ]

    for check_function, callback_function in mapping:
        if check_function(event):
            logging.debug('is %s event', check_function.__name__)
            return callback_function
    return common.skip_turn_handler
