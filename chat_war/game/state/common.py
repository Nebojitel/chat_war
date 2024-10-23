"""Check messages by patterns."""


from telethon import events

from chat_war.game.buttons import get_buttons_flat
from chat_war.game.parsers import strip_message

def is_hero_state(event: events.NewMessage.Event) -> bool:
    """Is hero info state."""
    message = strip_message(event.message.message)
    patterns = {
        'move speed:',
    }
    for pattern in patterns:
        if pattern in message:
            return True
    return False

def is_empty_energy(event: events.NewMessage.Event) -> bool:
    """Is empty energy state."""
    message = strip_message(event.message.message)
    return 'попробуй снова после отдыха' in message

def is_on_farm(event: events.NewMessage.Event) -> bool:
    """Is on farm state."""
    message = strip_message(event.message.message)
    patterns = {
        'position:',
    }
    for pattern in patterns:
        if pattern in message:
            return True
    return False

def farm_is_started(event: events.NewMessage.Event) -> bool:
    """Is farming started state."""
    message = strip_message(event.message.message)
    patterns = {
        'ты собираешься проверить близлежащие земли',
    }
    for pattern in patterns:
        if pattern in message:
            return True
    return False

def farm_is_finished(event: events.NewMessage.Event) -> bool:
    """Is farming finished state."""
    message = strip_message(event.message.message)
    patterns = {
        'исследование завершено',
    }
    for pattern in patterns:
        if pattern in message:
            return True
    return False

def farm_is_continued(event: events.NewMessage.Event) -> bool:
    """Is farming finished state."""
    message = strip_message(event.message.message)
    patterns = {
        'твое приключение продолжается',
    }
    for pattern in patterns:
        if pattern in message:
            return True
    return False
