import xbmc
import xbmcaddon
import time
import threading

def enable_addons():
    time.sleep(5)
    addons = ['plugin.video.torrest', 'plugin.video.opencodeplayer']
    for addon_id in addons:
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"' + addon_id + '","enabled":true},"id":1}')
        time.sleep(1)
    xbmc.log("[AutoEnable] Addons enabled", xbmc.LOGINFO)

t = threading.Thread(target=enable_addons)
t.daemon = True
t.start()

monitor = xbmc.Monitor()
while not monitor.abortRequested():
    if monitor.waitForAbort(10):
        break
