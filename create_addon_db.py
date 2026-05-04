import sqlite3, os, shutil
from datetime import datetime

src_db = r'C:\Users\user\Workspace\kodi_all_in_one_app\Marmalade_Android_Final3_backup_202605041713\userdata\Database\Addons33.db'
dst_db = r'C:\Users\user\Workspace\kodi_all_in_one_app\decompiled_marmalade\assets\userdata\Database\Addons33.db'

# Copy the existing database
shutil.copy2(src_db, dst_db)

# Connect and add entries
conn = sqlite3.connect(dst_db)
cursor = conn.cursor()

# Check if addon already exists in installed table
cursor.execute("SELECT addonID, enabled FROM installed")
existing = {row[0]: row[1] for row in cursor.fetchall()}

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
origin_uuid = 'b6a50484-93a0-4afb-a01c-8d17e059feda'  # Same as other addons

addons_to_add = [
    ('plugin.video.torrest', 1),
    ('plugin.video.opencodeplayer', 1),
]

for addon_id, enabled in addons_to_add:
    if addon_id not in existing:
        cursor.execute(
            "INSERT INTO installed (addonID, enabled, installDate, lastUpdated, lastUsed, origin, disabledReason) VALUES (?, ?, ?, NULL, NULL, ?, 0)",
            (addon_id, enabled, now, origin_uuid)
        )
        print(f"Added {addon_id} (enabled={enabled})")
    else:
        current = existing[addon_id]
        if current == 0:
            cursor.execute("UPDATE installed SET enabled=1, disabledReason=0 WHERE addonID=?", (addon_id,))
            print(f"Re-enabled {addon_id}")
        else:
            print(f"{addon_id} already enabled")

conn.commit()
conn.close()
print("Done!")
