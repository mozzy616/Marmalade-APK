import urllib.request
import re
import json

# Test scraping thepiratebay0.org
url = 'https://thepiratebay0.org/search/2025/0/7/207'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=10)
html = resp.read().decode('utf-8')

# Extract rows - each torrent is in a <div class="detWrap"> or similar
# Let's look at the structure more carefully
rows = re.findall(r'<div class="detName">.*?</td>\s*</tr>', html, re.DOTALL)
print('Rows found:', len(rows))

if rows:
    row = rows[0]
    name = re.search(r'class="detLink"[^>]*>(.*?)</a>', row)
    magnet = re.search(r'href="(magnet:\?[^"]+)"', row)
    seeds = re.findall(r'<td[^>]*>(\d+)</td>', row)
    size = re.search(r'Size (\S+)', row)
    
    print('Name:', name.group(1) if name else 'N/A')
    print('Magnet:', magnet.group(1)[:80] if magnet else 'N/A')
    print('Seeds:', seeds[:3] if seeds else 'N/A')
    print('Size:', size.group(1) if size else 'N/A')
