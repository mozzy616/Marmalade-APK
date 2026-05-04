import xbmc
import time

def enable_addon(addon_id):
    for attempt in range(5):
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"' + addon_id + '","enabled":true},"id":1}')
        time.sleep(1)
        result = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.GetAddonDetails","params":{"addonid":"' + addon_id + '","properties":["enabled"]},"id":2}')
        if '"enabled":true' in result:
            break
        time.sleep(2)

enable_addon('plugin.video.torrest')
enable_addon('plugin.video.opencodeplayer')
