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

## StreamLord Addon (plugin.video.streamlord)
- **Torrent-only** playback via CocoScrapers + torrest (no hosters/embeds)
- Movies: CocoScrapers (32 scrapers) → YTS API → TPB API → error dialog
- TV Shows: CocoScrapers (by IMDB ID from thumb) → TPB (by Show S01E01 title search) → error dialog
- IMDB ID extracted from thumb filename `/thumbs/XXXXXXX.jpg` + multiple HTML regex patterns
- Torrest daemon on port 61235, magnets built with trackers: opentrackr.org, stealth.si, torrent.eu.org
- CocoScrapers scrapers have only `sources(self, data, hostDict)` — no `movie()`/`tvshow()` methods
- `scraper_manager.py` instantiates scraper class before calling `sources()`, passes `{'imdb', 'title', 'year', 'aliases'}` dict
- Module path manually added to `sys.path`: `xbmcvfs.translatePath("special://home/addons/script.module.cocoscrapers/lib")`

## Key Fix: Torrest Enabled by Default
The `custom_build.zip` database had no Torrest entries. Fixed by updating `userdata/Database/Addons33.db` inside `custom_build.zip`:
- Added `plugin.video.torrest` to `installed` table with `enabled=1, disabledReason=0`
- Added `plugin.video.opencodeplayer` to `installed` table with `enabled=1, disabledReason=0`
- Added `service.autoenable` addon to `assets/addons/` that force-enables both addons via Kodi JSON-RPC on startup

## Directory Structure
- `decompiled_marmalade/` - Working decompiled APK (base = Marmalade Build Free.apk)
- `temp_custom/` - Addons that go into custom_build.zip
- `Marmalade_Android_Final3_backup_202605041713/` - Working backup userdata/settings

## Cloudnestra Embed Resolver (cloudnestra.py)
- Resolves streamdb.top → cloudnestra.com/rcp/ → cloudnestra.com/prorcp/ → HLS master.m3u8
- Embed chain: streamlord API → `vid.streamdb.top` (has iframe) → `cloudnestra.com/rcp/<hash>` (has JS with `/prorcp/` hash) → `/prorcp/<hash>` (has Playerjs with HLS URL)
- Playerjs config in `/prorcp/` page: `file: "https://tmstr3.{v1}/pl/H4sIAAAAAAAA.../master.m3u8 or ..."`
- Template vars `{v1}`-`{v5}` resolve to CDN domain `cloudnestra.com` (hardcoded in `SERVER_DOMAINS` dict)
- Master playlist returns 3 variants: 360p (916kbps), 720p (3.37Mbps), 1080p (6.45Mbps)
- Segments served from separate CDN (`cadenceofcognition.space` — auto-referenced in variant playlists)
- `play_embed_video()`: runs `resolve_embed_chain` first → if final URL is cloudnestra RCP, calls `cn.resolve(RCP_url)` → `_rcp_to_prorcp()` → `_extract_hls()` → plays via `_play_hls()` with inputstream.adaptive
- Falls back to `resolve_vidsrc(html)` → `resolve_with_resolveurl(embed_url)` → `resolve_with_resolveurl(final_url)`
- `fetch_raw()` now uses global `opener` (cookie jar) so cookies persist through embed chain
- `resolve_embed_chain()` now tracks correct `ref` per hop instead of always using BASE

## Fight Sports (watchwrestling.ae)
- Menu item `[B]Fight Sports[/B]` → 15 categories (WWE, AEW, UFC, Boxing, etc.)
- Each category lists recent posts with title + thumbnail, paginated
- Post detail page shows labeled video links (Dailymotion HD 720P, TopHd 720P, Ok Video HD 720P, etc.)
- Embed chain: snaptik.ae → fastvid.xyz → Dailymotion embed (resolveurl or dailymotion plugin)
- `watchwrestling.py` handles: `list_category()`, `get_post_detail()`, `resolve_video()`
- Dailymotion playback: try resolveurl first, fallback to `plugin.video.dailymotion`
- Direct HLS/mp4 links play via inputstream.adaptive

## XPrime Addon (plugin.video.xprime)
- **Content Browsing**: Uses TMDB API for movies, TV shows, trending, genres, and search
- **Source Type Selector**: User picks "Torrent (CocoScrapers)" or "Web Links (LeVidia)"
- **Torrent Playback**: CocoScrapers → Torrest REST API (pre-buffer 5MB min) → `http://127.0.0.1:61235/torrents/{hash}/files/{id}/serve` with fallback to `plugin://plugin.video.torrest/play_magnet`
- **Torrent Download**: Torrest (wait completion → copy via serve URL) or Real-Debrid (add magnet → select files → download via RD API)
- **Web Links (LeVidia)**: Scrapes `yuppow.app` (embedded by levidia.vip) — extracts 13 embed providers (vidking, vidlink, videasy, autoembed, vidsrc, embed.su, etc.) from `data-provider-url` attributes. Falls back to constructing embed URLs directly. Resolved via custom `GenericEmbedResolver` resolveurl plugin (covers all 13 providers). Falls back to direct URL playback if resolveurl fails.
- **resolveurl plugin**: `C:\Users\user\AppData\Roaming\Kodi\addons\script.module.resolveurl\lib\resolveurl\plugins\genericembed.py` — GenericEmbedResolver with domain matching for all 13 embed providers. Uses `helpers.scrape_sources()` + JS unpacking + iframe recursion. Special handlers for 2embed.cc (iframe chain → streamsrcs → packed JS → HLS) and vidsrc-embed.ru (cloudnestra iframe chain).
- **Settings**: Real-Debrid / AllDebrid / Premiumize API tokens, download folder picker

## Open Roms Addon (plugin.program.openroms)
- **Version**: 1.0.0, ID: `plugin.program.openroms`, provides `video game`
- **ROM Path**: Configured in addon settings, defaults to `D:\R36S Backups\EASYROMS 128gig Card`
- **Systems**: Maps 100+ system directories to display names, file extensions, and game.libretro.* core IDs
- **Organization**: Systems grouped by console family (Nintendo, Sega, Sony, Arcade, etc.) in the main menu
- **ROM Listing**: Each system shows ROMs filtered by valid extensions, with file size display
- **Launch Modes**:
  - **RetroPlayer (default)**: Sets `gameclient` property on ListItem → Kodi loads the appropriate Libretro core
  - **External RetroArch**: Configures RetroArch executable path and cores directory, launches via command line
- **Search**: Full ROM search across all system directories (up to 500 results)
- **Controller Profiles**: Per-system controller selection (NES, SNES, Genesis, N64, PlayStation) with 40+ game.controller.* addons bundled
- **BIOS Check**: Settings button to scan BIOS directory and report status; BIOS path configurable
- **BIOS**: User's R36S card has complete BIOS collection at `D:\R36S Backups\EASYROMS 128gig Card\bios\` — covers PlayStation, Saturn, Dreamcast, Neo Geo, Amiga, 3DO, MSX, PC Engine, and many more

## Bundled Libretro Cores (40 cores, downloaded from Kodi Omega mirror / RetroArch buildbot)
| Core | Systems | Size |
|------|---------|------|
| `game.libretro.fbneo` | Arcade, CPS1-3, Neo Geo (already bundled) | 20MB |
| `game.libretro.snes9x` | SNES / Super Famicom | 1.9MB |
| `game.libretro.nestopia` | NES / Famicom / FDS | 1.4MB |
| `game.libretro.genplus` | Genesis / Mega Drive / Master System / Game Gear / SG-1000 / Sega CD | 2.0MB |
| `game.libretro.gambatte` | Game Boy / Game Boy Color | 1.0MB |
| `game.libretro.mgba` | Game Boy Advance | 1.2MB |
| `game.libretro.mupen64plus-nx` | Nintendo 64 | 2.6MB |
| `game.libretro.beetle-psx` | PlayStation | 1.2MB |
| `game.libretro.flycast` | Dreamcast / NAOMI / Atomiswave | 2.1MB |
| `game.libretro.beetle-saturn` | Sega Saturn | 1.7MB |
| `game.libretro.beetle-pce` | PC Engine / TurboGrafx-16 / PCE CD | 1.3MB |
| `game.libretro.bluemsx` | MSX / MSX2 / ColecoVision | 1.1MB |
| `game.libretro.fuse` | ZX Spectrum | 1.2MB |
| `game.libretro.vice` | Commodore 64 / 128 / VIC-20 | 1.4MB |
| `game.libretro.dosbox` | DOS Games | 0.8MB |
| `game.libretro.dosbox-pure` | DOS Games (better) | 1.6MB |
| `game.libretro.prboom` | Doom engine | 0.9MB |
| `game.libretro.scummvm` | ScummVM games | **99MB** |
| `game.libretro.melonds` | Nintendo DS | 0.8MB |
| `game.libretro.desmume` | Nintendo DS (alt) | 1.0MB |
| `game.libretro.pcsx-rearmed` | PlayStation (lighter) | 0.7MB |
| `game.libretro.picodrive` | Sega 32X / Mega Drive (light) | 1.7MB |
| `game.libretro.stella` | Atari 2600 | 1.2MB |
| `game.libretro.atari800` | Atari 800 / 5200 / XEGS | 0.6MB |
| `game.libretro.hatari` | Atari ST | 0.8MB |
| `game.libretro.opera` | 3DO | 0.2MB |
| `game.libretro.fceumm` | NES (alt) | 1.2MB |
| `game.libretro.bsnes` | SNES (accuracy) | 1.8MB |
| `game.libretro.bsnes-hd` | SNES HD | 1.7MB |
| `game.libretro.mame2003_plus` | Arcade MAME | 9.5MB |
| `game.libretro.mame2003` | Arcade MAME | 7.7MB |
| `game.libretro.mame2000` | Arcade MAME | 2.8MB |
| `game.libretro.beetle-lynx` | Atari Lynx | 0.7MB |
| `game.libretro.beetle-ngp` | Neo Geo Pocket | 0.9MB |
| `game.libretro.beetle-wswan` | WonderSwan | 0.8MB |
| `game.libretro.handy` | Atari Lynx (alt) | 0.7MB |
| `game.libretro.beetle-vb` | Virtual Boy | 0.4MB |
| `game.libretro.daphne` | Laserdisc games | 1.5MB |
| `game.libretro.beetle-pce-fast` | PC Engine (fast) | 1.3MB |
| `game.libretro.ppsspp` | PSP (RetroArch buildbot) | 13.6MB |

## Bundled Controller Definitions (40 controllers)
All from Kodi Omega repo: NES, SNES (inc. mouse/multitap/super scope), N64, GameCube, PlayStation (original/dualshock/gamepad), Dreamcast, Saturn (inc. multitap/mouse/sticks/guns), Genesis/3b/6b, Master System, Game Gear, Game Boy, GBA, Atari 2600/5200/7800/800/Lynx/XEGS, ColecoVision, PC Engine, PC-FX, NGP, PSP, DS, VB, WS, Vectrex, Pokémini, Neo Geo Arcade, Xbox 360, SG-1000

## Build Status
- `plugin.program.openroms` registered in `Addons33.db` (enabled=1), added to `service.autoenable`
- All 40 game.libretro.* + 40 game.controller.* addons downloaded & registered (enabled=1)
- External Tools: BIOS packs at https://github.com/Abdess/retrobios (7,302 verified files, 396 systems)
- RetroPlayer Reference: https://github.com/garbear/xbmc-retroplayer (archived, documents game API)

## Important Notes
- **DO NOT** modify Open Code Player `main.py` - working version is in backup `addons/plugin.video.opencodeplayer/main.py`
- **DO NOT** add `set_fanart()` with `xbmcgui.Window(HANDLE)` - crashes the addon
- **DO NOT** use `xbmc.translatePath()` in Kodi 21 - use `xbmcvfs.translatePath()` instead
- Original `assets/addons/` must contain only Kodi built-in addons (no third-party addons)
- Third-party addons are delivered via `custom_build.zip` extracted by `service.build.extractor`
- Always clean `decompiled_marmalade/build` before rebuilding
- CocoScrapers `script.module.cocoscrapers` must be manually enabled in Kodi addon manager (installed but may be disabled)
- Torrest `plugin.video.torrest` must be enabled and daemon running on port 61235
- TV shows without IMDB numbers in thumb filename fall back to TPB search by title + S01E01

## Open Roms (plugin.program.openroms) - RetroPlayer State

### Known Working
- **SNES** (game.libretro.snes9x): zips extracted to .smc, routes via getGameInfoTag().setGameClient()
- **Genesis/Mega Drive** (game.libretro.genplus): zips extracted to .md, works
- **Master System / Game Gear** (game.libretro.genplus): zips extracted, works
- **NES** (game.libretro.nestopia): zips extracted to .nes, works
- **Game Boy / GBC** (game.libretro.gambatte): zips extracted to .gb/.gbc, works
- **Game Boy Advance** (game.libretro.mgba): zips extracted to .gba, works
- **Atari 2600** (game.libretro.stella): zips extracted to .a26, works
- **Sega 32X** (game.libretro.picodrive): zips extracted, works
- **Sega CD** (game.libretro.genplus): zips extracted to .bin/.iso, works
- **Arcade/MAME** (game.libretro.mame2003): works for MAME 0.78 compatible ROMs

### Known Broken
- **Nintendo 64** (game.libretro.mupen64plus-nx): core crashes Kodi on Windows (`requires_opengl=true`). Use External RetroArch mode in addon settings.
- **Dreamcast** (game.libretro.flycast/reicast): `No stream implementation for type: 3` on Windows. Use CHD format or External RetroArch mode.
- **Arcade CPS / Neo Geo**: ROM set version mismatch with installed cores (fbneo 1.0.0.99 needs different ROM version than R36S card). Try External RetroArch mode for these.

### Zip Handling Strategy
- **Non-arcade zips** (SNES, NES, Genesis, N64, GB/GBA, etc.): Extracted to temp dir, first non-metadata file (.smc, .nes, .md, .n64, .gb, etc.) passed to core. Native extension ensures RetroPlayer routing.
- **Arcade zips** (fbneo, mame cores): Original .zip passed directly. Core opens zip internally to read multiple ROM chip files. Routing via `getGameInfoTag().setGameClient()` which overrides VideoPlayer for known game cores.
- VFS=true cores (snes9x, nestopia, mupen64plus-nx, etc.): Extraction bypasses Kodi VFS layer; core gets raw file.

### Zip Handling Strategy
- **Non-arcade zips** (SNES, NES, Genesis, N64, GB/GBA, etc.): Extracted to temp dir, first non-metadata file (.smc, .nes, .md, .n64, .gb, etc.) passed to core. Native extension ensures RetroPlayer routing.
- **Arcade zips** (fbneo, mame cores): Original .zip passed directly. Core opens zip internally to read multiple ROM chip files. Routing via `getGameInfoTag().setGameClient()` which overrides VideoPlayer for known game cores.
- VFS=true cores (snes9x, nestopia, mupen64plus-nx, etc.): Extraction bypasses Kodi VFS layer; core gets raw file.

### Key Code Patterns
```python
# Critical: use getGameInfoTag().setGameClient(), NOT setProperty('gameclient', ...)
li = xbmcgui.ListItem(path=file_path)
tag = li.getGameInfoTag()
tag.setGameClient(core_id)              # 'game.libretro.snes9x'
li.setProperty('IsPlayable', 'true')    # enables play in UI
li.setProperty('game.controller', controller_id)  # optional controller binding
xbmc.Player().play(actual_path, li)
```
