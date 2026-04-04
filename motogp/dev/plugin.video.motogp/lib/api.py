"""MotoGP Pulselive API client."""

import json
import urllib.request
import urllib.error
import urllib.parse
import xbmc
import xbmcaddon

ADDON = xbmcaddon.Addon()

API_BASE = 'https://api.pulselive.motogp.com'
CONTENT_BASE = f'{API_BASE}/content/motogp'
MOTOGP_BASE = f'{API_BASE}/motogp/v1'

HEADERS = {
    'Accept': 'application/json',
    'Origin': 'https://www.motogp.com',
    'Referer': 'https://www.motogp.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

# Category UUIDs → display names (UUIDs vary per season/event)
# We detect category from video title if UUID is unknown
CATEGORY_NAMES = {
    '737ab122-76e1-4081-bedb-334caaa18c70': 'MotoGP',
    'ea854a67-73a4-4a28-ac77-d67b3b2a530a': 'Moto2',
    '1ab203aa-e292-4842-8bed-971911357af1': 'Moto3',
    '93888447-8746-4161-882c-e08a1d48447e': 'MotoGP',
    'bc2b0143-1bfb-4ad0-9501-da2e474e3ea7': 'Moto2',
    '7b0adf61-0a93-4e3d-a7ef-1fee93c2591f': 'Moto3',
}

SESSION_LABELS = {
    'RAC': 'Race',
    'SPR': 'Sprint',
    'Q1': 'Qualifying 1',
    'Q2': 'Qualifying 2',
    'FP1': 'Free Practice 1',
    'FP2': 'Free Practice 2',
    'FP3': 'Free Practice 3',
    'PR': 'Practice',
    'WUP': 'Warm Up',
}


def log(msg):
    if ADDON.getSetting('debug_log') == 'true':
        xbmc.log(f'[MotoGP] api: {msg}', xbmc.LOGINFO)


def _request(url, auth=False):
    """Make an HTTP GET request. If auth=True, include the DAT cookie."""
    log(f'GET {url}')
    req = urllib.request.Request(url)
    for k, v in HEADERS.items():
        req.add_header(k, v)

    if auth:
        token = ADDON.getSetting('auth_token').strip()
        if not token:
            raise RuntimeError('No auth token configured. Go to Add-on Settings → Authentication.')
        req.add_header('Cookie', f'DAT={token}')

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read().decode('utf-8')
            return json.loads(data)
    except urllib.error.HTTPError as e:
        if e.code == 401 or e.code == 403:
            raise RuntimeError('Auth token expired or invalid. Please update it in settings.')
        raise RuntimeError(f'API error: HTTP {e.code}')
    except urllib.error.URLError as e:
        raise RuntimeError(f'Network error: {e.reason}')


# ── Public API (no auth) ──

def get_events(season_year):
    """Get all events/races for a season."""
    url = f'{MOTOGP_BASE}/events?seasonYear={season_year}'
    return _request(url)


def get_event(event_id):
    """Get event details."""
    url = f'{MOTOGP_BASE}/events/{event_id}'
    return _request(url)


def get_videos_for_event(event_id, lang='en'):
    """Get all videos for an event by searching content API."""
    url = (f'{CONTENT_BASE}/video/{lang}/?offset=0&limit=100'
           f'&tagExpression=%22premium%22&references=MOTOGP_EVENT:{event_id}')
    return _request(url)


def get_video_metadata(content_id, lang='en'):
    """Get video metadata by content ID."""
    url = f'{CONTENT_BASE}/video/{lang}/{content_id}'
    return _request(url)


# ── Authenticated API ──

def get_player_data(video_uuid, protocol='dash'):
    """Get stream URLs for a video. Requires auth."""
    url = f'{MOTOGP_BASE}/video-gateway/video/{video_uuid}/player-data?protocol={protocol}'
    return _request(url, auth=True)


# ── Helpers ──

def get_event_name(event):
    """Extract a readable event name."""
    name = event.get('name', '').strip()
    short_name = event.get('short_name', '')
    country = event.get('country', '')
    circuit = event.get('circuit') or {}
    circuit_name = circuit.get('name', '')
    if name:
        return name.title()
    if short_name:
        return short_name
    if circuit_name:
        return f'{circuit_name} ({country})'
    return country or 'Unknown Event'


def get_event_poster(event):
    """Get event poster/thumbnail URL."""
    circuit = event.get('circuit', {})
    country = event.get('country', '')
    # Events don't have direct thumbnails; use a flag or circuit image if available
    return ''


def get_video_thumbnail(video):
    """Extract thumbnail from video metadata."""
    thumb = video.get('thumbnailUrl', '')
    if thumb and '?' not in thumb:
        thumb += '?width=640'
    elif thumb and 'width=' not in thumb:
        thumb += '&width=640'
    return thumb


def get_session_label(code):
    """Convert session code to readable label."""
    return SESSION_LABELS.get(code, code)


def get_category_name(category_id, title=''):
    """Convert category UUID to display name. Falls back to title detection."""
    name = CATEGORY_NAMES.get(category_id)
    if name:
        return name
    # Fallback: detect from video title
    if title:
        lower = title.lower()
        if 'moto3' in lower:
            return 'Moto3'
        if 'moto2' in lower:
            return 'Moto2'
        if 'motogp' in lower or 'after the flag' in lower:
            return 'MotoGP'
    return 'Other'
