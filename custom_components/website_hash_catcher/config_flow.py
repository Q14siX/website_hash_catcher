import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import SelectSelector, SelectSelectorConfig, SelectSelectorMode
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, CONF_URL, CONF_INTERVAL, CONF_NAME, CONF_HASH_TYPE, DEFAULT_INTERVAL, DEFAULT_HASH_TYPE, HASH_TYPES

class WebsiteHashFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Website Hash Catcher."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_NAME): cv.string,
            vol.Required(CONF_URL): cv.string,
            vol.Optional(CONF_INTERVAL, default=DEFAULT_INTERVAL): cv.positive_int,
            vol.Optional(
                CONF_HASH_TYPE,
                default=DEFAULT_HASH_TYPE
            ): SelectSelector(
                SelectSelectorConfig(
                    options=HASH_TYPES,
                    mode=SelectSelectorMode.DROPDOWN,
                    translation_key="hash_type"
                )
            ),
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
