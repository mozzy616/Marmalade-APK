import os

path = os.path.join('decompiled_kodi_new', 'smali', 'org', 'xbmc', 'kodi', 'Splash$FillCache.smali')
with open(path, 'r') as f:
    content = f.read()

idx = content.find('.method protected doInBackground')
print(f"Method declaration: {repr(content[idx:idx+100])}")

lines = content.split('\n')
for i in range(105, 115):
    if i < len(lines):
        print(f"  Line {i+1}: {repr(lines[i])}")
