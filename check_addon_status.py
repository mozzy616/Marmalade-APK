import sqlite3
db_path = r'C:\Users\user\Workspace\kodi_all_in_one_app\decompiled_marmalade\assets\userdata\Database\Addons33.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT addonID, enabled FROM installed WHERE addonID IN ('plugin.video.torrest', 'plugin.video.opencodeplayer', 'plugin.video.elementum')")
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()
