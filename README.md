# LGE Refrigerator

<p align="center">
  <img src="assets/logo.webp" alt="LGE Refrigerator" width="160">
</p>

Standalone HACS integration for **LG ThinQ Wi-Fi refrigerators**. It supports
refrigerators only: no washers, air conditioners, or other LG appliances are
created.

It includes a native HomeKit accessory. Apple Home sees one `Refrigerador`
accessory with its services grouped together, without Home Assistant's generic
HomeKit bridge and without a second LG polling client.

## Entities

For each selected refrigerator, the integration creates:

- `climate`: refrigerator and freezer controls, using the model's real target
  temperature range.
- `binary_sensor`: door-open status.
- `sensor`: refrigerator and freezer temperatures.
- `switch`: Ice Plus, Express Freezer, Express Fridge, and Eco Friendly when
  supported by the model.
- `sensor`: remaining water-filter and fresh-air-filter life when supported by
  the model.

In HomeKit, these are exposed through one accessory with refrigerator and freezer
thermostat services, the door sensor, available switches, and water-filter
maintenance when the model supports it.

## Installation with HACS

1. In HACS, go to **Integrations** → the ⋮ menu → **Custom repositories**.
2. Add `https://github.com/tdalejandro/lge_refrigerator_hacs` with the
   **Integration** category.
3. Install **LGE Refrigerator** and restart Home Assistant.
4. Go to **Settings** → **Devices & services** → **Add integration** →
   **LGE Refrigerator**.

The setup flow asks for your LG ThinQ account country and language. For accounts
created with Google, Apple, Facebook, or Amazon, enable browser-based sign-in.
Your password is never stored; Home Assistant stores only LG's renewable token.

The default HomeKit port is `21100`. Before pairing, Home Assistant displays a
notification with the HomeKit QR code and fallback PIN. The notification is
removed automatically after pairing.

## LG rate limits

LG may temporarily block accounts that are polled too frequently. This
integration uses a fixed 300-second interval and shares that single state between
the Home Assistant entities and the HomeKit accessory.

Before enabling this integration, disable or remove any previous SmartThinQ
instance that uses the same account to avoid duplicate LG requests.

## Credits and license

The vendored ThinQ client is based on
[ollo69/ha-smartthinq-sensors](https://github.com/ollo69/ha-smartthinq-sensors).
The refrigerator service design references
[nVuln/homebridge-lg-thinq](https://github.com/nVuln/homebridge-lg-thinq).
Both are distributed under Apache-2.0; see [NOTICE](NOTICE).
