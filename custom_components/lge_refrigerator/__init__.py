"""LGE Refrigerator: direct LG ThinQ and standalone HomeKit integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady

from .const import DATA_COORDINATOR, DATA_HOMEKIT, DOMAIN, PLATFORMS
from .coordinator import LGERefrigeratorCoordinator
from .homekit import LGERefrigeratorHomeKitBridge, LGERefrigeratorHomeKitQrView
from .vendor.wideq.core_exceptions import AuthenticationError, InvalidCredentialError

_LOGGER = logging.getLogger(__name__)

LGERefrigeratorConfigEntry = ConfigEntry


async def async_setup_entry(
    hass: HomeAssistant, entry: LGERefrigeratorConfigEntry
) -> bool:
    """Set up one LG ThinQ refrigerator and its single HomeKit accessory."""
    view_key = f"{DOMAIN}_homekit_qr_view"
    if view_key not in hass.data:
        hass.http.register_view(LGERefrigeratorHomeKitQrView(hass))
        hass.data[view_key] = True

    try:
        coordinator = await LGERefrigeratorCoordinator.async_create(hass, entry)
    except ConfigEntryAuthFailed:
        raise
    except (AuthenticationError, InvalidCredentialError) as err:
        raise ConfigEntryNotReady("LG ThinQ authentication is not currently available") from err
    except ValueError as err:
        _LOGGER.error("The selected LG appliance is not an available refrigerator: %s", err)
        return False
    except Exception as err:
        raise ConfigEntryNotReady("Unable to initialize the LG ThinQ refrigerator") from err

    try:
        homekit = await LGERefrigeratorHomeKitBridge.async_create(
            hass, entry, coordinator
        )
        hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
            DATA_COORDINATOR: coordinator,
            DATA_HOMEKIT: homekit,
        }
        await homekit.async_start()
    except OSError as err:
        hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
        await coordinator.async_close()
        raise ConfigEntryNotReady(
            f"Unable to bind HomeKit port {entry.data['homekit_port']}"
        ) from err

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: LGERefrigeratorConfigEntry
) -> bool:
    """Unload entities, mDNS advertisement, HomeKit listener, and ThinQ client."""
    if not await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        return False

    data = hass.data[DOMAIN].pop(entry.entry_id)
    await data[DATA_HOMEKIT].async_stop()
    await data[DATA_COORDINATOR].async_close()
    return True
