import zipfile, os, tempfile, sqlite3
os.chdir('C:/Users/user/Workspace/kodi_all_in_one_app')
with zipfile.ZipFile('kodi_marmalade_unsigned-aligned-debugSigned.apk', 'r') as zf:
    data = zf.read('assets/userdata/Database/Addons33.db')
    tmp_path = os.path.join(tempfile.gettempdir(), 'check.db')
    with open(tmp_path, 'wb') as f:
        f.write(data)
    conn = sqlite3.connect(tmp_path)
    cursor = conn.cursor()
    cursor.execute("SELECT addonID, enabled, disabledReason FROM installed WHERE addonID LIKE '%extractor%' OR addonID LIKE '%build%'")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()
    os.remove(tmp_path)
