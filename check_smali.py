import glob

files = glob.glob(r'decompiled_kodi_new\smali\org\xbmc\kodi\Splash*.smali')
for f in files:
    print(f"File: {f}")
    with open(f, 'r') as fh:
        content = fh.read()
    for i, line in enumerate(content.split('\n')):
        if '.locals' in line and i < 20:
            print(f"  Line {i+1}: {line.strip()}")
        if 'copy_done' in line or 'FileInputStream' in line or 'copy_loop' in line:
            print(f"  Line {i+1}: {line.strip()}")
