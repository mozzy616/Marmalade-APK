import zipfile, os, sqlite3, tempfile
os.chdir('C:/Users/user/Workspace/kodi_all_in_one_app')
with zipfile.ZipFile('kodi_marmalade_unsigned-aligned-debugSigned.apk', 'r') as zf:
    data = zf.read('assets/userdata/Database/Addons33.db')
    tmp_path = os.path.join(tempfile.gettempdir(), 'check_apk_db.db')
    with open(tmp_path, 'wb') as f:
        f.write(data)

conn = sqlite3.connect(tmp_path)
cursor = conn.cursor()
cursor.execute("SELECT addonID, enabled, disabledReason FROM installed WHERE addonID LIKE '%torrest%' OR addonID LIKE '%opencode%'")
rows = cursor.fetchall()
print('--- Torrest/Opencodeplayer in APK DB ---')
for row in rows:
    print(row)

autoexec = zf.read('assets/userdata/autoexec.py').decode('utf-8')
print('\n--- autoexec.py ---')
print(autoexec)

conn.close()
os.remove(tmp_path)
