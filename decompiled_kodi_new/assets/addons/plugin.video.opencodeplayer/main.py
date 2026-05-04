import xbmcgui
import xbmcplugin
import sys
import xbmc
import xbmcvfs
import os

def show_menu():
    li = xbmcgui.ListItem("[B]Open a Torrent[/B]")
    li.setInfo("video", {"title": "Open a Torrent"})
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), "plugin://plugin.video.opencodeplayer/?action=open", li, isFolder=False)

    li = xbmcgui.ListItem("[B]Paste from Clipboard[/B]")
    li.setInfo("video", {"title": "Paste from Clipboard"})
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), "plugin://plugin.video.opencodeplayer/?action=clip", li, isFolder=False)

    li = xbmcgui.ListItem("[B]Select Text File[/B]")
    li.setInfo("video", {"title": "Select Text File"})
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), "plugin://plugin.video.opencodeplayer/?action=browse", li, isFolder=False)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def action_open():
    clip = xbmc.getInfoLabel("System.Clipboard")
    default = ""
    if clip and (clip.startswith("magnet:") or ".torrent" in clip.lower()):
        default = clip

    k = xbmc.Keyboard(default, "Paste magnet link here")
    k.doModal()

    if k.isConfirmed():
        link = k.getText().strip()
        if link:
            xbmcgui.Dialog().ok("Link Received", "Link: " + link[:80])
        else:
            xbmcgui.Dialog().ok("Empty", "No link entered.")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def action_clip():
    clip = xbmc.getInfoLabel("System.Clipboard")
    if clip and (clip.startswith("magnet:") or ".torrent" in clip.lower()):
        xbmcgui.Dialog().ok("Found", "Clipboard: " + clip[:80])
    else:
        xbmcgui.Dialog().ok("No Link", "Copy a magnet link on Android first, then try again.")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def action_browse():
    dialog = xbmcgui.Dialog()
    
    paths = dialog.browseSingle(
        1,
        "Select text file with magnet link",
        "files",
        ".txt",
        False,
        False,
        "special://home/"
    )
    
    if paths and xbmcvfs.exists(paths):
        f = xbmcvfs.File(paths)
        link = f.read().strip()
        f.close()
        
        if link:
            if dialog.yesno("Link Found", "Read link:\n" + link[:80] + "\n\nPlay now?"):
                pass
            else:
                xbmcplugin.endOfDirectory(int(sys.argv[1]))
                return
        else:
            dialog.ok("Empty", "File is empty.")
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
            return
    else:
        dialog.ok("Cancelled", "No file selected.")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        return

def main():
    p = {}
    if len(sys.argv) > 2 and sys.argv[2].startswith("?"):
        for part in sys.argv[2][1:].split("&"):
            if "=" in part:
                k, v = part.split("=", 1)
                p[k] = v
    a = p.get("action", "")
    if a == "open":
        action_open()
    elif a == "clip":
        action_clip()
    elif a == "browse":
        action_browse()
    else:
        show_menu()

if __name__ == "__main__":
    main()
