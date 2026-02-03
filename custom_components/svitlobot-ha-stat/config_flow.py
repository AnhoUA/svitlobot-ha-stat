"""Config flow for Svitlobot integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import CITY_KYIV, DOMAIN

CITIES = {
    "Київ": "Київ",
    "Харків": "Харків",
    "Одеса": "Одеса",
    "Дніпро": "Дніпро",
    "Львів": "Львів",
    "Запоріжжя": "Запоріжжя",
    "Вінниця": "Вінниця",
    "Полтава": "Полтава",
    "Чернігів": "Чернігів",
    "Суми": "Суми",
}


class SvitlobotConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Svitlobot."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            city = user_input.get("city", CITY_KYIV)

            # Check if already configured for this city
            await self.async_set_unique_id(f"svitlobot_{city}")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"Svitlobot {city}",
                data={"city": city},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("city", default=CITY_KYIV): vol.In(CITIES),
                }
            ),
            errors=errors,
        )
