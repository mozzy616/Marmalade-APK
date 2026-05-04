import sqlite3, os, json
from datetime import datetime

db_path = r'C:\Users\user\Workspace\kodi_all_in_one_app\decompiled_marmalade\assets\userdata\Database\Addons33.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if torrest is in addons table
cursor.execute("SELECT addonID FROM addons WHERE addonID='plugin.video.torrest'")
row = cursor.fetchone()

if not row:
    # Torrest metadata as JSON (matching Kodi format)
    metadata = json.dumps({
        "art": {"icon": "https://raw.githubusercontent.com/i96751414/plugin.video.torrest/master/icon.png"},
        "author": "i96751414",
        "dependencies": [
            {"addonId": "script.module.requests", "minversion": "2.22.0", "optional": False, "version": "2.22.0"},
            {"addonId": "script.module.routing", "minversion": "0.2.3", "optional": False, "version": "0.2.3"}
        ],
        "disclaimer": "",
        "extensions": [
            {
                "children": [],
                "type": "xbmc.python.pluginsource",
                "values": [{"content": [{"key": "@library", "value": "navigation.py"}], "id": ""}, {"content": [{"key": "@provides", "value": "video"}], "id": "provides"}]
            },
            {
                "children": [],
                "type": "xbmc.service",
                "values": [{"content": [{"key": "@library", "value": "service.py"}], "id": ""}]
            }
        ],
        "extrainfo": [],
        "icon": "icon.png",
        "lifecycledesc": "",
        "lifecycletype": 0,
        "path": "special://home/addons/plugin.video.torrest",
        "screenshots": ["resources/screenshots/screenshot-1.jpg", "resources/screenshots/screenshot-2.jpg"],
        "size": 0
    })

    cursor.execute("INSERT INTO addons (metadata, addonID, version, name, summary, news, description) VALUES (?, 'plugin.video.torrest', '0.0.22', 'Torrest', 'Torrest on Kodi', 'Update torrest binary to v0.0.8', 'Torrest is a service with a rest API which allows torrent streaming.')", (metadata,))
    print("Added Torrest to addons table")
else:
    print("Torrest already in addons table")

# Verify
cursor.execute("SELECT addonID, version, enabled FROM addons WHERE addonID='plugin.video.torrest'")
row = cursor.fetchone()
print("addons table:", row)

cursor.execute("SELECT addonID, enabled, disabledReason FROM installed WHERE addonID='plugin.video.torrest'")
row = cursor.fetchone()
print("installed table:", row)

conn.commit()
conn.close()
