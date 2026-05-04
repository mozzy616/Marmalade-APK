import zipfile, os, tempfile, sqlite3
os.chdir('C:/Users/user/Workspace/kodi_all_in_one_app')
with zipfile.ZipFile('decompiled_marmalade/assets/custom_build.zip', 'r') as zf:
    data = zf.read('userdata/Database/Addons33.db')
    tmp_path = os.path.join(tempfile.gettempdir(), 'check_build_db.db')
    with open(tmp_path, 'wb') as f:
        f.write(data)
    conn = sqlite3.connect(tmp_path)
    cursor = conn.cursor()
    cursor.execute("SELECT addonID, enabled, disabledReason FROM installed WHERE addonID LIKE '%torrest%' OR addonID LIKE '%opencode%'")
    rows = cursor.fetchall()
    print('Torrest/Opencodeplayer in build DB installed table:')
    for row in rows:
        print(' ', row)
    
    cursor.execute("SELECT addonID, version FROM addons WHERE addonID LIKE '%torrest%'")
    rows = cursor.fetchall()
    print('\nTorrest in build DB addons table:')
    for row in rows:
        print(' ', row)
    
    conn.close()
    os.remove(tmp_path)
