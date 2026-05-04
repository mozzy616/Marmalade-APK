# Kodi All-in-One Build - Marmalade Build Free

## Current Build
- **APK:** `kodi_marmalade_unsigned-aligned-debugSigned.apk` (~399MB)
- **Source:** `Marmalade Build Free.apk` (decompiled to `decompiled_marmalade/`)
- **Signed:** Debug certificate via uber-apk-signer

## How to Build
```
java -jar apktool.jar b decompiled_marmalade -o kodi_marmalade_unsigned.apk
java -jar uber-apk-signer.jar -a kodi_marmalade_unsigned.apk
```

## Key Fix: Torrest Enabled by Default
The `custom_build.zip` database had no Torrest entries. Fixed by updating `userdata/Database/Addons33.db` inside `custom_build.zip`:
- Added `plugin.video.torrest` to `installed` table with `enabled=1, disabledReason=0`
- Added `plugin.video.opencodeplayer` to `installed` table with `enabled=1, disabledReason=0`
- Added `service.autoenable` addon to `assets/addons/` that force-enables both addons via Kodi JSON-RPC on startup

## Directory Structure
- `decompiled_marmalade/` - Working decompiled APK (base = Marmalade Build Free.apk)
- `temp_custom/` - Addons that go into custom_build.zip
- `Marmalade_Android_Final3_backup_202605041713/` - Working backup userdata/settings

## Important Notes
- **DO NOT** modify Open Code Player `main.py` - working version is in backup `addons/plugin.video.opencodeplayer/main.py`
- **DO NOT** add `set_fanart()` with `xbmcgui.Window(HANDLE)` - crashes the addon
- **DO NOT** use `xbmc.translatePath()` in Kodi 21 - use `xbmcvfs.translatePath()` instead
- Original `assets/addons/` must contain only Kodi built-in addons (no third-party addons)
- Third-party addons are delivered via `custom_build.zip` extracted by `service.build.extractor`
- Always clean `decompiled_marmalade/build` before rebuilding
