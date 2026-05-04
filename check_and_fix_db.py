import sqlite3

db_path = r'C:\Users\user\Workspace\kodi_all_in_one_app\Marmalade_Android_Final3_backup_202605041713\userdata\Database\Addons33.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT addonID, enabled FROM installed WHERE addonID LIKE '%torrest%' OR addonID LIKE '%opencode%' OR addonID LIKE '%elementum%'")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Check all addons that are disabled (enabled=0)
print("\n--- Disabled addons ---")
cursor.execute("SELECT addonID, enabled FROM installed WHERE enabled=0")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Force enable torrest and opencodeplayer
cursor.execute("UPDATE installed SET enabled=1, disabledReason=0 WHERE addonID LIKE '%torrest%'")
cursor.execute("UPDATE installed SET enabled=1, disabledReason=0 WHERE addonID LIKE '%opencode%'")
conn.commit()

print("\n--- After fix ---")
cursor.execute("SELECT addonID, enabled FROM installed WHERE addonID LIKE '%torrest%' OR addonID LIKE '%opencode%'")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
