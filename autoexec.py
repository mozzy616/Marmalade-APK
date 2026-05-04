import xbmc
import xbmcvfs
import os
import shutil

def copy_db():
    home = xbmcvfs.translatePath("special://home/")
    xbmpath = xbmcvfs.translatePath("special://xbmc/")
    src = os.path.join(xbmpath, "userdata", "Database", "Addons33.db")
    dst_dir = os.path.join(home, "userdata", "Database")
    dst = os.path.join(dst_dir, "Addons33.db")
    
    xbmc.log(f"[autoexec] home={home}", xbmc.LOGINFO)
    xbmc.log(f"[autoexec] xbmc={xbmpath}", xbmc.LOGINFO)
    xbmc.log(f"[autoexec] src={src}", xbmc.LOGINFO)
    xbmc.log(f"[autoexec] dst={dst}", xbmc.LOGINFO)
    
    if xbmcvfs.exists(dst):
        xbmc.log("[autoexec] DB already exists, skipping", xbmc.LOGINFO)
        return
    
    if not xbmcvfs.exists(src):
        xbmc.log("[autoexec] Source DB not found", xbmc.LOGWARNING)
        return
    
    if not xbmcvfs.exists(dst_dir):
        os.makedirs(dst_dir)
    
    xbmc.log("[autoexec] Copying Addons33.db...", xbmc.LOGINFO)
    if xbmcvfs.copy(src, dst):
        xbmc.log("[autoexec] DB copied successfully", xbmc.LOGINFO)
        xbmc.executebuiltin("ReloadProfile")
    else:
        xbmc.log("[autoexec] Failed to copy DB", xbmc.LOGFATAL)

if __name__ == "__main__":
    copy_db()
