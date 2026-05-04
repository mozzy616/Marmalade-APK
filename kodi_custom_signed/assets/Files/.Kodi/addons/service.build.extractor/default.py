import xbmc
import xbmcgui
import xbmcvfs
import os
import zipfile

def install_custom_build():
    # Paths
    home_dir = xbmcvfs.translatePath("special://home/")
    temp_dir = xbmcvfs.translatePath("special://temp/")
    flag_file = os.path.join(home_dir, "build_installed.txt")
    
    # Source zip in the APK assets
    source_zip_vfs = "special://xbmc/custom_build.zip"
    temp_zip_path = os.path.join(temp_dir, "custom_build.zip")
    
    xbmc.log("BuildExtractor: Checking if build needs installation...", xbmc.LOGINFO)
    
    # Check if already installed
    if not os.path.exists(flag_file):
        xbmc.log("BuildExtractor: Flag file not found. Starting installation.", xbmc.LOGINFO)
        
        # Check if the zip exists in the installation assets
        if xbmcvfs.exists(source_zip_vfs):
            xbmc.log("BuildExtractor: Source zip found in assets.", xbmc.LOGINFO)
            dialog = xbmcgui.DialogProgress()
            dialog.create("Custom Build", "Installing custom build. Please wait...")
            
            try:
                # Copy zip from read-only APK assets to writable temp dir
                dialog.update(10, "Copying files...")
                xbmcvfs.copy(source_zip_vfs, temp_zip_path)
                
                # Extract zip
                dialog.update(40, "Extracting build...")
                with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
                    zip_ref.extractall(home_dir)
                
                # Clean up temp zip
                os.remove(temp_zip_path)
                
                # Write flag file so it doesn't extract again
                with open(flag_file, 'w') as f:
                    f.write("Installed")
                
                dialog.update(100, "Installation Complete! Restarting...")
                xbmc.sleep(3000)
                
                # Force restart/quit to load new addons and userdata
                xbmc.executebuiltin("Quit")
                
            except Exception as e:
                xbmc.log(f"BuildExtractor Error: {str(e)}", xbmc.LOGFATAL)
                dialog.update(100, f"Error: {str(e)}")
                xbmc.sleep(5000)
            
            dialog.close()
        else:
            xbmc.log("BuildExtractor: Could not find custom_build.zip in special://xbmc/", xbmc.LOGWARNING)

if __name__ == '__main__':
    install_custom_build()