# """Sensor platform for integration_blueprint."""

# from __future__ import annotations

# from typing import TYPE_CHECKING, List

# import decimal

# from homeassistant.components.fan import (
#     FanEntity,
#     FanEntityDescription,
#     FanEntityFeature,
# )

# from .data import Berluf_selen_500_ConfigEntry
# from .defs import LOGGER
# from .entity import Berluf_selen_500_Entry

# from .berluf_selen_500.funcs import Supply_fan, Exhaust_fan

# if TYPE_CHECKING:
#     from homeassistant.core import HomeAssistant
#     from homeassistant.helpers.entity_platform import AddEntitiesCallback


# async def async_setup_entry(
#     hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
#     entry: Berluf_selen_500_ConfigEntry,
#     async_add_entities: AddEntitiesCallback,
# ) -> None:
#     """Set up the fan platform."""
#     async_add_entities(
#         [
#             Berluf_selen_500_fan(
#                 fan_class=Supply_fan,
#                 entry=entry,
#                 entity_description=FanEntityDescription(
#                     key="berluf_selen_500",
#                     name="Berluf Selen 500 supply fan",
#                     # icon="mdi:format-quote-close",
#                 ),
#             ),
#             # Berluf_selen_500_fan(
#             #     fan_class=Exhaust_fan,
#             #     entry=entry,
#             #     entity_description=FanEntityDescription(
#             #         key="berluf_selen_500",
#             #         name="Berluf Selen 500 exhaust fan",
#             #         # icon="mdi:format-quote-close",
#             #     ),
#             # ),
#         ]
#     )


# class Berluf_selen_500_fan(Berluf_selen_500_Entry, FanEntity):
#     """berluf_selen_500 fan."""

#     def __init__(
#         self,
#         fan_class,
#         entry: Berluf_selen_500_ConfigEntry,
#         entity_description: FanEntityDescription,
#     ) -> None:
#         """Initialize the sensor class."""
#         super().__init__(entry)
#         self._attr_supported_features = FanEntityFeature.SET_SPEED

#         self.entity_description = entity_description
#         self._impl = fan_class(entry.runtime_data.get_device())

#     def set_percentage(self, percentage: int) -> None:
#         """Set the speed percentage of the fan."""
#         self._impl.set(percentage)

#     @property
#     def percentage(self) -> int | None:
#         """Return the current speed as a percentage."""
#         return self._impl.get()
