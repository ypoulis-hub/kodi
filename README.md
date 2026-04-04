# Kodi Add-ons

A collection of custom Kodi add-ons for streaming premium content.

---

## Add-ons

### 🎵 YTMusic — YouTube Music for Kodi (`plugin.audio.ytmusic`)

Browse and play your YouTube Music Premium library directly in Kodi. No external dependencies — uses the YouTube Innertube API directly.

**Features**
- Home feed with personalized recommendations
- Full library: playlists, albums, artists, liked songs, history
- Search with filters (songs, albums, artists, playlists)
- Artist pages with top songs, albums, and singles
- Lyrics display
- Radio / watch playlist (auto-queues similar tracks)
- Brand account switching
- Background stream prefetching for gapless-ish playback
- Audio quality selection (Best / 256kbps / 128kbps / 64kbps)

**Requirements**
- Kodi 21 (Omega) or later
- YouTube Music Premium subscription
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) installed on the system (or auto-installed by the add-on)

**Authentication**

This add-on uses browser cookies for authentication — no passwords are stored.

1. Install a browser cookie export extension:
   - Chrome: *Get cookies.txt LOCALLY*
   - Firefox: *cookies.txt*
2. Log in to [music.youtube.com](https://music.youtube.com)
3. Export cookies to a `cookies.txt` file (Mozilla/Netscape format)
4. In Kodi, go to **Add-on Settings → Authentication → Re-import cookies.txt** and select the file

**Settings**

| Setting | Description |
|--------|-------------|
| Brand Account Page ID | For YouTube brand/channel accounts (leave empty for personal account) |
| Re-import cookies.txt | Import a new cookies file |
| Audio Quality | Best / High (256kbps) / Medium (128kbps) / Low (64kbps) |
| Items per page | 25 / 50 / 100 |
| Custom Python path | Override yt-dlp Python path (leave empty for auto-detect) |
| Debug logging | Enable verbose logging to Kodi log |

---

### 🏍️ MotoGP VideoPass (`plugin.video.motogp`)

Browse and play MotoGP, Moto2, and Moto3 races with your VideoPass subscription. Supports multiple camera feeds and up to 1080p@50fps via adaptive streaming.

**Features**
- Browse all seasons back to 2012
- Races, sprint races, qualifying sessions, practice sessions
- Multiple camera feeds per session:
  - Commentary (main broadcast)
  - Ambient (no commentary)
  - Helicopter camera
  - Onboard cameras 1–4
- Video quality selection (1080p / 720p / 540p / 360p)
- Adaptive DASH streaming via `inputstream.adaptive`

**Requirements**
- Kodi 21 (Omega) or later
- [inputstream.adaptive](https://github.com/xbmc/inputstream.adaptive) add-on (included with most Kodi builds)
- MotoGP VideoPass subscription ([motogp.com/en/videopass](https://www.motogp.com/en/videopass))

**Authentication**

The add-on uses your VideoPass session token (DAT cookie).

1. Log in to [motogp.com/en/videopass](https://www.motogp.com/en/videopass) in your browser
2. Press **F12** → **Application** → **Cookies** → find the `DAT` cookie
3. Copy its value
4. In Kodi, go to **Add-on Settings → Authentication → Auth Token** and paste it

The token is a JWT and the add-on will warn you when it expires.

**Settings**

| Setting | Description |
|--------|-------------|
| Auth Token | Your DAT cookie value from motogp.com |
| Max Video Quality | 1080p / 720p / 540p / 360p |
| Default Camera Feed | Commentary / Ambient / Helicopter / Onboard 1–4 |
| Default Season Year | Pre-select a season on startup (empty = current year) |
| Debug logging | Enable verbose logging to Kodi log |

---

## Installation

1. Download the zip for the add-on you want from the `vX.Y.Z/` folder
2. In Kodi: **Settings → Add-ons → Install from zip file**
3. Navigate to the downloaded zip and install
4. Follow the authentication steps above for each add-on

---

## License

MIT
