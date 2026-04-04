"""Stream URL resolver using system Python + yt-dlp."""

import subprocess
import json
import os
import xbmc
import xbmcaddon

ADDON = xbmcaddon.Addon()


def log(msg):
    xbmc.log('[YTMusic] resolver: {}'.format(msg), xbmc.LOGINFO)


def _find_system_python():
    """Find system Python 3 (not Kodi's bundled one)."""
    candidates = ['python3', 'python', 'py']

    # Common Windows Python locations
    local_appdata = os.environ.get('LOCALAPPDATA', '')
    if local_appdata:
        python_base = os.path.join(local_appdata, 'Programs', 'Python')
        if os.path.isdir(python_base):
            for sub in os.listdir(python_base):
                exe = os.path.join(python_base, sub, 'python.exe')
                if os.path.isfile(exe):
                    candidates.insert(0, exe)
        # Also check pythoncore (Windows Store / winget)
        for entry in os.listdir(local_appdata):
            if entry.lower().startswith('python'):
                sub = os.path.join(local_appdata, entry)
                if os.path.isdir(sub):
                    for item in os.listdir(sub):
                        exe = os.path.join(sub, item, 'python.exe')
                        if os.path.isfile(exe):
                            candidates.insert(0, exe)

    for candidate in candidates:
        try:
            result = subprocess.run(
                [candidate, '-c', 'import yt_dlp; print("ok")'],
                capture_output=True, text=True, timeout=10,
                creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0),
            )
            if result.returncode == 0 and 'ok' in result.stdout:
                log('Found system Python with yt-dlp: {}'.format(candidate))
                return candidate
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue

    return None


_system_python = None


def get_system_python():
    global _system_python
    if _system_python is None:
        _system_python = _find_system_python()
    return _system_python


def get_stream_url(video_id):
    """Resolve a stream URL by calling yt-dlp via system Python."""
    python = get_system_python()
    if not python:
        raise RuntimeError(
            'Cannot find system Python with yt-dlp installed. '
            'Install yt-dlp: pip install yt-dlp'
        )

    url = 'https://music.youtube.com/watch?v={}'.format(video_id)

    # Run yt-dlp as a subprocess using system Python
    script = (
        'import yt_dlp, json, sys; '
        'ydl_opts = {"format": "bestaudio", "quiet": True, "no_warnings": True, "noplaylist": True}; '
        'ydl = yt_dlp.YoutubeDL(ydl_opts); '
        'info = ydl.extract_info(sys.argv[1], download=False); '
        'print(json.dumps({"url": info.get("url",""), "title": info.get("title",""), '
        '"artist": info.get("artist", info.get("uploader","")), '
        '"duration": info.get("duration",0), '
        '"bitrate": info.get("abr",0)}))'
    )

    log('Resolving stream for video_id={}'.format(video_id))

    try:
        result = subprocess.run(
            [python, '-c', script, url],
            capture_output=True, text=True, timeout=30,
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0),
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError('Stream resolution timed out.')

    if result.returncode != 0:
        log('yt-dlp error: {}'.format(result.stderr[:300]))
        raise RuntimeError('yt-dlp failed: {}'.format(result.stderr[:200]))

    try:
        info = json.loads(result.stdout.strip())
    except (json.JSONDecodeError, ValueError):
        log('Bad yt-dlp output: {}'.format(result.stdout[:200]))
        raise RuntimeError('yt-dlp returned invalid output.')

    stream_url = info.get('url', '')
    if not stream_url:
        raise RuntimeError('No stream URL returned by yt-dlp.')

    log('Resolved: {} ({} bps)'.format(stream_url[:80], info.get('bitrate', '?')))
    return stream_url, info
