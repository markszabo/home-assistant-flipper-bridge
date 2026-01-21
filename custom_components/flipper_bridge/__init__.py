import logging
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry

from .const import (
    DOMAIN,
    CONF_PORT,
    CONF_BAUDRATE,
    SERVICE_SEND_CLI,
    ATTR_COMMAND,
    ATTR_RESPONSE,
)
from .serial_client import FlipperSerialClient

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    client = FlipperSerialClient(
        port=entry.data[CONF_PORT],
        baudrate=entry.data[CONF_BAUDRATE],
    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = client

    async def handle_send_cli(call: ServiceCall):
        command = call.data[ATTR_COMMAND]

        response = await hass.async_add_executor_job(
            client.send_command, command
        )

        return {ATTR_RESPONSE: response}

    hass.services.async_register(
        DOMAIN,
        SERVICE_SEND_CLI,
        handle_send_cli,
        schema={
            ATTR_COMMAND: str,
        },
        supports_response=True,
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    client = hass.data[DOMAIN].pop(entry.entry_id)
    await hass.async_add_executor_job(client.close)
    return True
