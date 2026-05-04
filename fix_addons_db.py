import sqlite3
import os
from datetime import datetime

db_path = 'custom_build/userdata/Database/Addons33.db'
addons_dir = 'custom_build/addons'

# Get list of addon IDs in custom_build/addons
addon_ids = [d for d in os.listdir(addons_dir) if os.path.isdir(os.path.join(addons_dir, d))]

print(f'Found {len(addon_ids)} addons in custom_build/addons')

db = sqlite3.connect(db_path)
c = db.cursor()

# Get existing addon IDs
c.execute("SELECT addonID FROM installed")
existing = set(r[0] for r in c.fetchall())
print(f'Found {len(existing)} existing addons in DB')

SYSTEM_ORIGIN = 'b6a50484-93a0-4afb-a01c-8d17e059feda'
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

for addon_id in sorted(addon_ids):
    if addon_id not in existing:
        c.execute("INSERT INTO installed (addonID, enabled, installDate, lastUpdated, lastUsed, origin, disabledReason) VALUES (?, 1, ?, ?, ?, ?, 0)",
                  (addon_id, now, now, now, SYSTEM_ORIGIN))
        print(f'  Added {addon_id}')

db.commit()

# Verify
c.execute("SELECT addonID, enabled FROM installed ORDER BY addonID")
for row in c.fetchall():
    print(f'  {row[0]}: enabled={row[1]}')

db.close()
print('\nDone')
