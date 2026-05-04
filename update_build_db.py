import zipfile, os, tempfile, sqlite3, shutil
from datetime import datetime

os.chdir('C:/Users/user/Workspace/kodi_all_in_one_app')

# Read the DB from custom_build.zip
with zipfile.ZipFile('decompiled_marmalade/assets/custom_build.zip', 'r') as zf:
    data = zf.read('userdata/Database/Addons33.db')
    tmp_path = os.path.join(tempfile.gettempdir(), 'temp_build_db.db')
    with open(tmp_path, 'wb') as f:
        f.write(data)

# Update the DB
conn = sqlite3.connect(tmp_path)
cursor = conn.cursor()
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
origin_uuid = 'b6a50484-93a0-4afb-a01c-8d17e059feda'

# Check if Torrest exists in installed
cursor.execute("SELECT enabled FROM installed WHERE addonID='plugin.video.torrest'")
row = cursor.fetchone()
if not row:
    cursor.execute("INSERT INTO installed (addonID, enabled, installDate, lastUpdated, lastUsed, origin, disabledReason) VALUES ('plugin.video.torrest', 1, ?, NULL, NULL, ?, 0)", (now, origin_uuid))
    print("Added Torrest to installed table")
else:
    cursor.execute("UPDATE installed SET enabled=1, disabledReason=0 WHERE addonID='plugin.video.torrest'")
    print("Updated Torrest to enabled=1")

# Check Opencodeplayer
cursor.execute("SELECT enabled FROM installed WHERE addonID='plugin.video.opencodeplayer'")
row = cursor.fetchone()
if not row:
    cursor.execute("INSERT INTO installed (addonID, enabled, installDate, lastUpdated, lastUsed, origin, disabledReason) VALUES ('plugin.video.opencodeplayer', 1, ?, NULL, NULL, ?, 0)", (now, origin_uuid))
    print("Added Opencodeplayer to installed table")
else:
    cursor.execute("UPDATE installed SET enabled=1, disabledReason=0 WHERE addonID='plugin.video.opencodeplayer'")
    print("Updated Opencodeplayer to enabled=1")

conn.commit()

# Verify
cursor.execute("SELECT addonID, enabled, disabledReason FROM installed WHERE addonID IN ('plugin.video.torrest', 'plugin.video.opencodeplayer')")
rows = cursor.fetchall()
print("\nVerification:")
for row in rows:
    print(" ", row)

conn.close()

# Write back to custom_build.zip
shutil.copy2('decompiled_marmalade/assets/custom_build.zip', 'decompiled_marmalade/assets/custom_build.zip.bak')
with zipfile.ZipFile('decompiled_marmalade/assets/custom_build.zip', 'a') as zf:
    with open(tmp_path, 'rb') as f:
        zf.writestr('userdata/Database/Addons33.db', f.read())
print("\nUpdated custom_build.zip database")

os.remove(tmp_path)
