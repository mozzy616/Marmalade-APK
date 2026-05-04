import xbmc
import xbmcgui
import xbmcvfs
import os
import shutil
import zipfile

def install_custom_build():
    home_dir = xbmcvfs.translatePath("special://home/")
    temp_dir = xbmcvfs.translatePath("special://temp/")
    flag_file = os.path.join(home_dir, ".build_installed_flag")
    source_zip_vfs = "special://xbmc/custom_build.zip"
    temp_zip_path = os.path.join(temp_dir, "custom_build.zip")

    xbmc.log("[BuildExtractor] Starting...", xbmc.LOGINFO)

    if xbmcvfs.exists(flag_file):
        xbmc.log("[BuildExtractor] Already installed, skipping.", xbmc.LOGINFO)
        return

    if not xbmcvfs.exists(source_zip_vfs):
        xbmc.log("[BuildExtractor] Zip not found at special://xbmc/custom_build.zip", xbmc.LOGWARNING)
        return

    xbmc.log("[BuildExtractor] Installing custom build...", xbmc.LOGINFO)

    dialog = xbmcgui.DialogProgress()
    dialog.create("Custom Build", "Preparing installation...")

    try:
        dialog.update(5, "Copying archive...")
        if not xbmcvfs.copy(source_zip_vfs, temp_zip_path):
            raise Exception("Failed to copy zip from APK assets")

        dialog.update(20, "Extracting addons...")
        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        dialog.update(60, "Installing addons...")
        src_addons = os.path.join(temp_dir, "addons")
        dst_addons = os.path.join(home_dir, "addons")
        if os.path.exists(src_addons):
            for item in os.listdir(src_addons):
                src = os.path.join(src_addons, item)
                dst = os.path.join(dst_addons, item)
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)

        dialog.update(80, "Installing userdata...")
        src_userdata = os.path.join(temp_dir, "userdata")
        dst_userdata = os.path.join(home_dir, "userdata")
        if os.path.exists(src_userdata):
            if not os.path.exists(dst_userdata):
                os.makedirs(dst_userdata)
            for item in os.listdir(src_userdata):
                src = os.path.join(src_userdata, item)
                dst = os.path.join(dst_userdata, item)
                if os.path.exists(dst):
                    if os.path.isdir(dst):
                        shutil.rmtree(dst)
                    else:
                        os.remove(dst)
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)

        dialog.update(90, "Cleaning up...")
        for item in os.listdir(temp_dir):
            item_path = os.path.join(temp_dir, item)
            if item == "custom_build.zip":
                os.remove(item_path)
            elif item in ("addons", "userdata"):
                shutil.rmtree(item_path)

        with open(flag_file, 'w') as f:
            f.write("done")

        dialog.update(100, "Installation complete! Restarting...")
        xbmc.sleep(2000)
        xbmc.executebuiltin("ReloadProfile")

    except Exception as e:
        xbmc.log(f"[BuildExtractor] ERROR: {str(e)}", xbmc.LOGFATAL)
        dialog.update(100, f"Error: {str(e)}")
        xbmc.sleep(5000)

    dialog.close()

if __name__ == '__main__':
    install_custom_build()