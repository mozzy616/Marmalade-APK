import os

SMALI = os.path.join('decompiled_kodi_new', 'smali', 'org', 'xbmc', 'kodi', 'Splash$FillCache.smali')

with open(SMALI, 'r') as f:
    content = f.read()

# Check what line 111 is
lines = content.split('\n')
print(f"Line 111: {lines[110]}")
print(f"Line 108: {lines[107]}")

# Count all v registers used in the file's doInBackground method
# Find the start and end of doInBackground
start = content.find('.method protected doInBackground()Ljava/lang/Integer;')
# Find next method after doInBackground
next_method = content.find('.method ', start + 10)
method_body = content[start:next_method]

# Find all register references
import re
v_regs = set()
for m in re.find(r'v(\d+)', method_body):
    v_regs.add(int(m))
print(f"Max v register used in doInBackground: {max(v_regs)}")
print(f"Total unique v registers: {len(v_regs)}")
print(f"Registers used: {sorted(v_regs)}")
