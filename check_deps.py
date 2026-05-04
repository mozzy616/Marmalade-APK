import sqlite3

db_path = r'C:\Users\user\Workspace\kodi_all_in_one_app\decompiled_marmalade\assets\userdata\Database\Addons33.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check dependencies
cursor.execute("SELECT addonID, enabled FROM installed WHERE addonID IN ('script.module.requests', 'script.module.routing')")
rows = cursor.fetchall()
print("--- Torrest dependencies ---")
for row in rows:
    print(row)

# Check all enabled addons count
cursor.execute("SELECT COUNT(*) FROM installed WHERE enabled=1")
print("\nEnabled addons:", cursor.fetchone()[0])
cursor.execute("SELECT COUNT(*) FROM installed WHERE enabled=0")
print("Disabled addons:", cursor.fetchone()[0])

# List all addons that have enabled=0
print("\n--- All disabled addons ---")
cursor.execute("SELECT addonID, enabled, disabledReason FROM installed WHERE enabled=0")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
