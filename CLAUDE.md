# Kodi Addons

Custom Kodi addons workspace. Each addon has its own directory with `dev/` and versioned stable folders.

## Directory structure
```
KODI ADDON/
├── ytmusic/          # plugin.audio.ytmusic
│   ├── dev/          # active development
│   ├── v1.0.1/       # previous stable
│   ├── v1.0.4/       # previous stable
│   ├── v1.0.5/       # previous stable
│   ├── v1.0.6/       # previous stable
│   ├── v1.0.7/       # current stable — frozen, do not edit
│   └── *.zip         # release zips
└── motogp/           # plugin.video.motogp
    ├── dev/          # active development
    └── v0.1.0/       # current stable — frozen, do not edit
```

## Workflow
- Edit in `<addon>/dev/` → approve → promote to new `<addon>/vX.Y.Z/` stable, build zip, deploy to installed copies

---

## YTMusic (plugin.audio.ytmusic)

### Version management
- **Stable**: `ytmusic/v1.0.7/` — frozen, do not edit
- **Previous stable**: `ytmusic/v1.0.6/`, `ytmusic/v1.0.5/`, `ytmusic/v1.0.4/`, `ytmusic/v1.0.1/`
- **Dev**: `ytmusic/dev/` — all changes happen here

### Addon locations
- **Stable source**: `ytmusic/v1.0.7/plugin.audio.ytmusic/`
- **Stable zip**: `ytmusic/v1.0.7/plugin.audio.ytmusic.zip`
- **Dev source**: `ytmusic/dev/plugin.audio.ytmusic/`
- **Installed (local PC)**: `C:\Users\ypoul\AppData\Roaming\Kodi\addons\plugin.audio.ytmusic\`
- **Installed (LibreELEC)**: `root@192.168.1.35:/storage/.kodi/addons/plugin.audio.ytmusic/`
- **Installed (remote PC)**: `\\192.168.1.104\c$\Users\kodi\AppData\Roaming\Kodi\addons\plugin.audio.ytmusic\`
- Both installed copies track the current stable version

### Key facts
- Kodi 21 on both local (ypoul) and remote (kodi user) Windows PCs
- Uses system Python + yt-dlp subprocess for stream resolution (not Kodi's bundled Python 3.8)
- System Python path: `C:\Users\ypoul\AppData\Local\Python\pythoncore-3.14-64\python.exe`
- YouTube Music cookies stored at: `special://profile/cookies.txt` (resolved via `xbmcvfs.translatePath()`)
- Remote PC accessible via UNC: `\\192.168.1.104\c$`

### Stream resolution (resolver.py)
- yt-dlp called as subprocess with `format: bestaudio`
- Cookies file used for Premium 256kbps quality
- Falls back to no-cookies if yt-dlp fails with cookies (yt-dlp EJS challenge issues)
- `yt-dlp[default]` package required for EJS challenge solver: `pip install yt-dlp[default]`

---

## MotoGP (plugin.video.motogp)

### Version management
- **Stable**: `motogp/v0.1.0/` — frozen, do not edit
- **Dev**: `motogp/dev/` — all changes happen here

### Addon locations
- **Stable source**: `motogp/v0.1.0/plugin.video.motogp/`
- **Stable zip**: `motogp/v0.1.0/plugin.video.motogp.zip`
- **Dev source**: `motogp/dev/plugin.video.motogp/`
- **Installed (local PC)**: `C:\Users\ypoul\AppData\Roaming\Kodi\addons\plugin.video.motogp\`
- **Installed (LibreELEC)**: `root@192.168.1.35:/storage/.kodi/addons/plugin.video.motogp/`

---

## Shared notes

### addon.xml requirements
- `xbmc.python` version must be `3.0.1` (not 3.0.0 — causes invalid structure on install)
- Must include `<assets><icon>icon.png</icon></assets>` in metadata for icon to show
- Bump version number before rebuilding zip or Kodi won't reinstall

### Zip build rules
- Do NOT include `setup_ytdlp.bat` in the zip (causes invalid structure error)
- Build with Python zipfile or PowerShell Compress-Archive
- After building, uninstall old version first OR bump version number

### Icon
- 256x256 RGB PNG (not RGBA)
- Clear Kodi texture cache after replacing: delete `Textures13.db` entries + `Thumbnails/` files

### Remote PC notes
- User: `kodi`
- `visualization.fishbmc` addon was disabled (renamed to .disabled) — was crashing Kodi on all audio
- Audio output: SoundMAX onboard
