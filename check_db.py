import sqlite3, os

db_path = r'C:\Users\user\Workspace\kodi_all_in_one_app\Marmalade_Android_Final3_backup_202605041713\userdata\Database\Addons33.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tables:', [t[0] for t in tables])

for table in tables:
    tname = table[0]
    cursor.execute("SELECT * FROM " + tname + " LIMIT 3")
    rows = cursor.fetchall()
    print('\nTable: ' + tname)
    if rows:
        cols = [d[0] for d in cursor.description]
        print('Columns:', cols)
        for row in rows:
            print(row)

conn.close()
