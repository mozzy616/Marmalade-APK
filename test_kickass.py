import urllib.request
import re

# Check search page more thoroughly for any hidden magnet data
url = 'https://kickass.sx/search/2025'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=10)
html = resp.read().decode('utf-8-sig')

# Look for data-hash or similar attributes on links
links = re.findall(r'<a[^>]*href="(/[^"]+\.html)"[^>]*class="cellMainLink"[^>]*>', html)
print('Torrent links:', len(links))
for link in links[:5]:
    print(' ', link)

# Check for seeders/leechers
seed_patterns = [
    r'<td[^>]*>\s*(\d+)\s*</td>',
    r'class="seed">(\d+)',
    r'green">(\d+)',
]
for pat in seed_patterns:
    matches = re.findall(pat, html)
    print(f'Pattern {pat}:', len(matches), matches[:3] if matches else '')
