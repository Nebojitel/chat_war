"""Telegram client."""

from telethon import TelegramClient

from chat_war.settings import app_settings

client = TelegramClient(
    session='.chat_war',
    api_id=app_settings.telegram_api_id,
    api_hash=app_settings.telegram_api_hash,
    auto_reconnect=True,
    connection_retries=app_settings.tlg_client_retries,
    retry_delay=app_settings.tlg_client_retry_delay,
    device_model='Desktop Tg Client',
)
