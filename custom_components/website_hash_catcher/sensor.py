import logging
import hashlib
import subprocess
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_URL, CONF_INTERVAL, CONF_NAME, CONF_HASH_TYPE, DEFAULT_HASH_TYPE, HASH_TYPES

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """Set up the Website Hash sensor from a config entry."""
    coordinator = WebsiteHashCoordinator(hass, entry.data)
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([WebsiteHashSensor(coordinator, entry)], True)

class WebsiteHashCoordinator(DataUpdateCoordinator):
    """Handles fetching the website hash periodically."""
    def __init__(self, hass: HomeAssistant, config):
        """Initialize the coordinator."""
        self.url = config[CONF_URL]
        self.hash_type = config.get(CONF_HASH_TYPE, DEFAULT_HASH_TYPE)
        update_interval = timedelta(seconds=config[CONF_INTERVAL])

        super().__init__(
            hass,
            _LOGGER,
            name="Website Hash Coordinator",
            update_interval=update_interval,
        )

    async def _async_update_data(self):
        """Fetch the latest hash from the website."""
        return await self.hass.async_add_executor_job(self._fetch_hash)

    def _fetch_hash(self):
        """Fetch and compute the hash."""
        try:
            result = subprocess.run(["curl", "-s", self.url], capture_output=True, text=True)
            if result.returncode == 0:
                raw_data = result.stdout.encode()
                if self.hash_type == "sha256":
                    return hashlib.sha256(raw_data).hexdigest()
                elif self.hash_type == "sha1":
                    return hashlib.sha1(raw_data).hexdigest()
                elif self.hash_type == "md5":
                    return hashlib.md5(raw_data).hexdigest()
                elif self.hash_type == "sha512":
                    return hashlib.md5(raw_data).hexdigest()
            else:
                _LOGGER.error("Error fetching website: %s", result.stderr)
        except Exception as e:
            _LOGGER.error("Error while fetching website hash: %s", e)
        return None

class WebsiteHashSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Website Hash sensor."""

    def __init__(self, coordinator: WebsiteHashCoordinator, entry: ConfigEntry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = entry.data[CONF_NAME]
        self._attr_unique_id = f"website_hash_{entry.entry_id}"
        self._attr_native_unit_of_measurement = None

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data
