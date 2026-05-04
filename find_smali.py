import re

with open(r'decompiled_clean\smali\org\xbmc\kodi\Splash$FillCache.smali', 'r') as f:
    content = f.read()
    lines = content.split('\n')

for i, line in enumerate(lines):
    if 'const/4 v1, 0x6' in line:
        print(f'Line {i+1}: {line}')
        for j in range(max(0,i-3), min(len(lines),i+8)):
            print(f'  {j+1}: {lines[j]}')
        print('---')
