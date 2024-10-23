"""Grinding handlers."""
import logging
from typing import Dict, List

from telethon import events
import asyncio

from chat_war import wait_utils
from chat_war.game import parsers
from chat_war.game.action import common
from chat_war.settings import app_settings, game_bot_name
from chat_war.telegram_client import client
from chat_war.game.buttons import GO_WEST, GO_EAST, GO_NORTH, GO_SOUTH, FIELD, FOREST, MOUNTAIN, CAMP, get_buttons_flat

available_buttons: Dict[str, List[str]] = {
    'farm_zone_buttons': [],
    'camp_zone_buttons': [],
}

async def processing(event: events.NewMessage.Event) -> None:
    """Начинаем что-то делать."""
    buttons = get_buttons_flat(event)

    if buttons:
        if any(FOREST in btn.text for btn in buttons):
            await start_farming(event)
        elif any(CAMP in btn.text for btn in buttons):
            await go_to_farming_zone(event)
    else:
        logging.warning(f'Кнопки для категории не найдены. Инициализация не выполнена.')


async def relaxing(event: events.NewMessage.Event) -> None:
    """Отдыхаем."""
    logging.info('Отдыхаем 3 часа.')
    await asyncio.sleep(3 * 3600)
    await common.show_hero(event)


async def update_available_buttons(event: events.NewMessage.Event, category: str) -> None:
    """Обновляем доступные кнопки по указанной категории."""
    global available_buttons
    buttons = get_buttons_flat(event)

    if buttons:
        if category == 'farm_zone_buttons':
            for btn in buttons:
                available_buttons['farm_zone_buttons'].append(btn.text)

        elif category == 'camp_zone_buttons':
            for btn in buttons:
                available_buttons['camp_zone_buttons'].append(btn.text)

        available_buttons = {key: list(set(val)) for key, val in available_buttons.items()}
    else:
        logging.warning(f'Кнопки для категории {category} не найдены. Обновление не выполнено.')


async def handle_button_event(button_symbol: str, category: str) -> bool:
    """Обрабатываем нажатие кнопки по символу из указанной категории."""
    global available_buttons
    buttons = available_buttons.get(category, [])
    button = next((btn for btn in buttons if button_symbol in btn), None)
    
    if button:
        await wait_utils.wait_for()
        await client.send_message(game_bot_name, button)
        return True
    logging.warning(f'Кнопка с символом "{button_symbol}" не найдена в категории {category}.')
    return False


async def go_to_farming_zone(event: events.NewMessage.Event) -> None:
    """Выбираем локацию для фарма"""
    await update_available_buttons(event, 'camp_zone_buttons')
    if any(CAMP in btn for btn in available_buttons['camp_zone_buttons']):
        logging.info('Идем в локацию.')
        await wait_utils.wait_for()
        button_to_press = next(btn for btn in available_buttons['camp_zone_buttons'] if CAMP in btn)
        await handle_button_event(button_to_press, 'camp_zone_buttons')
    else:
        logging.warning('Не удалось найти кнопку для перехода в локацию.')


async def start_farming(event: events.NewMessage.Event) -> None:
    """Начинаем фармить локацию."""
    await update_available_buttons(event, 'farm_zone_buttons')

    try:
        hp_level = parsers.get_hp_level(event.message.message)
        energy = parsers.get_energy(event.message.message)
        moves = parsers.get_character_moves(event.message.message)
    except Exception as e:
        logging.warning(f'Не удалось получить уровень энергии или здоровья: {e}')
        hp_level = None
        energy = None 
        moves = None   

    if hp_level <= app_settings.minimum_hp_level_for_grinding:
        logging.info('Мало хп, лечимся.')
        await asyncio.sleep(3600)
        await common.show_hero(event)
    elif energy <= 0:
        logging.info('Мало энергии, ждем 1 час.')
        await asyncio.sleep(3600)
        await common.show_hero(event)
    else:
        if any(FOREST in btn for btn in available_buttons['farm_zone_buttons']):
            logging.info('Начинаем фарм.')
            await wait_utils.wait_for()
            button_to_press = next(btn for btn in available_buttons['farm_zone_buttons'] if FOREST in btn)
            await handle_button_event(button_to_press, 'farm_zone_buttons')
        else:
            logging.warning('Не удалось найти кнопку начать фарм.')

