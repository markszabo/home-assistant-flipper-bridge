from homeassistant import config_entries
import voluptuous as vol
import serial.tools.list_ports

from .const import DOMAIN, CONF_PORT, CONF_BAUDRATE, DEFAULT_BAUDRATE


class FlipperBridgeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        ports = [
            port.device
            for port in serial.tools.list_ports.comports()
            if "Flipper" in port.description or "ACM" in port.device
        ]

        if not ports:
            errors["base"] = "no_device"

        if user_input is not None:
            return self.async_create_entry(
                title=f"Flipper ({user_input[CONF_PORT]})",
                data=user_input,
            )

        schema = vol.Schema({
            vol.Required(CONF_PORT): vol.In(ports),
            vol.Optional(CONF_BAUDRATE, default=DEFAULT_BAUDRATE): int,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
