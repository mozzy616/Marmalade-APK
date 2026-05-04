import sqlite3

db_path = r'C:\Users\user\Workspace\kodi_all_in_one_app\decompiled_marmalade\assets\userdata\Database\Addons33.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("--- Torrest/Opencodeplayer status ---")
cursor.execute("SELECT addonID, enabled, disabledReason FROM installed WHERE addonID LIKE '%torrest%' OR addonID LIKE '%opencode%'")
rows = cursor.fetchall()
for row in rows:
    print(row)

if not rows:
    print("Not found in DB! Checking all installed addons...")
    cursor.execute("SELECT addonID, enabled, disabledReason FROM installed LIMIT 20")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

conn.close()
