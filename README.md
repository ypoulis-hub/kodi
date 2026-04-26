# MotoGP VideoPass for Kodi

`plugin.video.motogp` — Browse and play MotoGP, Moto2, and Moto3 races with your VideoPass subscription. Supports multiple camera feeds and up to 1080p@50fps via adaptive streaming.

[![Donate with PayPal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/donate/?business=ypoulis%40gmail.com&currency_code=EUR)

---

## Features

- **Live race streaming** — watch the current live broadcast (race, qualifying, practice, etc.) when an event is on
- Browse all seasons back to 2012
- Races, sprint races, qualifying sessions, practice sessions
- Multiple camera feeds per session:
  - Commentary (main broadcast)
  - Ambient (no commentary)
  - Helicopter camera
  - Onboard cameras 1–4
- Video quality selection (1080p / 720p / 540p / 360p)
- Adaptive streaming via `inputstream.adaptive` — DASH for VOD, HLS for live

## Requirements

- Kodi 21 (Omega) or later
- [inputstream.adaptive](https://github.com/xbmc/inputstream.adaptive) add-on (included with most Kodi builds)
- MotoGP VideoPass subscription ([motogp.com/en/videopass](https://www.motogp.com/en/videopass))

## Installation

1. Download the zip from the `v0.2.0/` folder
2. In Kodi: **Settings → Add-ons → Install from zip file**
3. Navigate to the downloaded zip and install
4. Follow the authentication steps below

## Authentication

The add-on uses your VideoPass session token (DAT cookie).

1. Log in to [motogp.com/en/videopass](https://www.motogp.com/en/videopass) in your browser
2. Press **F12** → **Application** → **Cookies** → find the `DAT` cookie
3. Copy its value
4. In Kodi, go to **Add-on Settings → Authentication → Auth Token** and paste it

The token is a JWT and the add-on will warn you when it expires.

## Settings

| Setting | Description |
|--------|-------------|
| Auth Token | Your DAT cookie value from motogp.com |
| Max Video Quality | 1080p / 720p / 540p / 360p |
| Default Camera Feed | Commentary / Ambient / Helicopter / Onboard 1–4 |
| Default Season Year | Pre-select a season on startup (empty = current year) |
| Debug logging | Enable verbose logging to Kodi log |

## License

MIT

---

[![Donate with PayPal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/donate/?business=ypoulis%40gmail.com&currency_code=EUR)
