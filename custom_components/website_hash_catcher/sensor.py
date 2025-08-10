import logging
import hashlib
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    CoordinatorEntity,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    CONF_URL,
    CONF_INTERVAL,
    CONF_NAME,
    CONF_HASH_TYPE,
    DEFAULT_HASH_TYPE,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Website Hash sensors from a config entry."""
    name = entry.data.get(CONF_NAME) or "Website Hash"
    url = entry.data[CONF_URL]
    interval_seconds = int(entry.data.get(CONF_INTERVAL) or 60)
    hash_type = entry.data.get(CONF_HASH_TYPE) or DEFAULT_HASH_TYPE

    coordinator = WebsiteHashCoordinator(
        hass=hass,
        url=url,
        hash_type=hash_type,
        update_interval=timedelta(seconds=interval_seconds),
        logger=_LOGGER,
    )

    # Erstes Update abwarten, damit der Sensor direkt einen State hat
    await coordinator.async_config_entry_first_refresh()

    async_add_entities([WebsiteHashSensor(coordinator, entry, name)], True)


class WebsiteHashCoordinator(DataUpdateCoordinator[str | None]):
    """Coordinator to fetch and hash website content."""

    def __init__(
        self,
        hass: HomeAssistant,
        url: str,
        hash_type: str,
        update_interval: timedelta,
        logger: logging.Logger,
    ) -> None:
        super().__init__(
            hass,
            logger,
            name=f"{DOMAIN}_coordinator",
            update_interval=update_interval,
        )
        self._url = url
        self._hash_type = (hash_type or DEFAULT_HASH_TYPE).lower()

        # Prüfe, ob hashlib den gewünschten Algo kennt
        if not hasattr(hashlib, self._hash_type):
            logger.warning(
                "Unbekannter Hash-Typ '%s', falle zurück auf %s",
                self._hash_type,
                DEFAULT_HASH_TYPE,
            )
            self._hash_type = DEFAULT_HASH_TYPE

    async def _async_update_data(self) -> str | None:
        """Fetch website and compute hash."""
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(self._url, timeout=30) as resp:
                resp.raise_for_status()
                raw = await resp.read()
        except Exception as err:  # noqa: BLE001
            self.logger.error("Fehler beim Abruf von %s: %s", self._url, err)
            # None zurückgeben ⇒ Sensor bleibt vorhanden, state wird unknown
            return None

        hasher = getattr(hashlib, self._hash_type)
        return hasher(raw).hexdigest()


class WebsiteHashSensor(CoordinatorEntity[WebsiteHashCoordinator], SensorEntity):
    """Representation of a Website Hash sensor."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: WebsiteHashCoordinator, entry: ConfigEntry, name: str) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_name = name
        self._attr_unique_id = f"website_hash_{entry.entry_id}"
        # kein unit_of_measurement bei Hash
        self._attr_icon = "mdi:web"

    @property
    def native_value(self) -> str | None:
        # Neuer SensorEntity-API: native_value statt state
        return self.coordinator.data

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "url": self.coordinator._url,         # noqa: SLF001
            "hash_type": self.coordinator._hash_type,  # noqa: SLF001
            "interval": int(self.coordinator.update_interval.total_seconds()),
        }
