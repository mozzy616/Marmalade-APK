import sqlite3, os, json

db_path = r'C:\Users\user\Workspace\kodi_all_in_one_app\decompiled_marmalade\assets\userdata\Database\Addons33.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check current state
cursor.execute("SELECT addonID, version FROM addons WHERE addonID='plugin.video.torrest'")
row = cursor.fetchone()
print("Torrest in addons table:", row)

cursor.execute("SELECT addonID, enabled, disabledReason FROM installed WHERE addonID='plugin.video.torrest'")
row = cursor.fetchone()
print("Torrest in installed table:", row)

conn.close()
