# -*- coding: utf-8 -*-
"""
Lazy-loading libtorrent wrapper for Kodi Android.
No code executes on import - call init_libtorrent() when needed.
"""
import os
import sys
import xbmc
import xbmcvfs
import xbmcaddon

_libtorrent = None

def _log(msg):
    try:
        xbmc.log("[script.module.libtorrent] %s" % msg, level=xbmc.LOGINFO)
    except:
        pass

def init_libtorrent():
    """Initialize and return libtorrent module. Call this from your addon."""
    global _libtorrent
    if _libtorrent is not None:
        return _libtorrent

    __settings__ = xbmcaddon.Addon(id='script.module.libtorrent')
    addon_path = xbmc.translatePath(__settings__.getAddonInfo('path'))
    root = os.path.join(addon_path, 'python_libtorrent')

    # Detect platform
    system = None
    if xbmc.getCondVisibility("system.platform.android"):
        arch = "x86"
        try:
            import platform
            machine = platform.machine().lower()
            if "arm" in machine or "aarch64" in machine:
                arch = "arm"
        except:
            arch = "arm"

        if arch == "arm":
            system = "android_armv7"
        else:
            system = "android_x86"

    if not system:
        _log("Unsupported platform")
        return None

    _log("Platform: %s" % system)

    # Find latest version
    platform_dir = os.path.join(root, system)
    if not os.path.exists(platform_dir):
        _log("Platform dir not found: %s" % platform_dir)
        return None

    versions = [d for d in os.listdir(platform_dir) if os.path.isdir(os.path.join(platform_dir, d))]
    if not versions:
        _log("No versions found")
        return None

    version = sorted(versions)[-1]
    _log("Using version: %s" % version)

    # Copy libs to a writable temp dir (Android can't load .so from assets)
    dest_base = os.path.join(xbmc.translatePath('special://temp'), 'libtorrent_native')
    dest_path = os.path.join(dest_base, system, version)
    xbmcvfs.mkdirs(dest_path)

    src_path = os.path.join(platform_dir, version)

    # Copy libtorrent.so
    src_so = os.path.join(src_path, 'libtorrent.so')
    dst_so = os.path.join(dest_path, 'libtorrent.so')
    needs_copy = True
    if xbmcvfs.exists(dst_so):
        try:
            if os.path.getsize(src_so) == os.path.getsize(dst_so):
                needs_copy = False
        except:
            pass

    if needs_copy:
        if xbmcvfs.exists(dst_so):
            xbmcvfs.delete(dst_so)
        xbmcvfs.copy(src_so, dst_so)
        _log("Copied libtorrent.so to %s" % dest_path)

    # Copy liblibtorrent.so (required for Android preload)
    src_llt = os.path.join(src_path, 'liblibtorrent.so')
    dst_llt = os.path.join(dest_path, 'liblibtorrent.so')
    needs_copy_llt = True
    if xbmcvfs.exists(dst_llt):
        try:
            if os.path.getsize(src_llt) == os.path.getsize(dst_llt):
                needs_copy_llt = False
        except:
            pass

    if needs_copy_llt:
        if xbmcvfs.exists(dst_llt):
            xbmcvfs.delete(dst_llt)
        xbmcvfs.copy(src_llt, dst_llt)
        _log("Copied liblibtorrent.so to %s" % dest_path)

    # Workaround: copy to kodi lib dir if possible
    kodi_lib = '/data/data/org.xbmc.kodi/lib/'
    kodi_libtorrent = os.path.join(kodi_lib, 'liblibtorrent.so')
    try:
        if xbmcvfs.exists(kodi_lib):
            if not xbmcvfs.exists(kodi_libtorrent):
                xbmcvfs.copy(dst_llt, kodi_libtorrent)
                _log("Copied to kodi lib: %s" % kodi_libtorrent)
    except:
        pass

    # Preload liblibtorrent.so via ctypes so Python can find it
    from ctypes import CDLL
    try:
        _log("Loading liblibtorrent.so via CDLL")
        CDLL(dst_llt)
        _log("CDLL loaded successfully")
    except Exception as e:
        _log("CDLL failed: %s" % str(e))

    # Import the actual libtorrent Python module
    sys.path.insert(0, dest_path)
    try:
        import importlib.util
        lib_path = os.path.join(dest_path, 'libtorrent.so')
        spec = importlib.util.spec_from_file_location('libtorrent', lib_path)
        _libtorrent = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_libtorrent)
        _log("libtorrent v%s loaded successfully" % _libtorrent.version)
        return _libtorrent
    except Exception as e:
        _log("Failed to import libtorrent: %s" % str(e))
        return None

def get_libtorrent():
    """Get the libtorrent module (initializes if needed)."""
    return init_libtorrent()
