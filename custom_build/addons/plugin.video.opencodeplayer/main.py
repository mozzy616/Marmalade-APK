import xbmcgui
import xbmcplugin
import xbmc
import sys
import json
import re
import urllib.request
import urllib.parse
import threading
import os

HANDLE = int(sys.argv[1])
URL = sys.argv[0]
PARAMS = sys.argv[2]

# Get addon path for fanart
ADDON_PATH = xbmc.translatePath('special://home/addons/plugin.video.opencodeplayer/')
FANART_PATH = os.path.join(ADDON_PATH, 'fanart.jpg')

API_BASE = "https://apibay.org"
TPB_BASE = "https://thepiratebay0.org"
KICKASS_BASE = "https://kickass.sx"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
MOVIE_CAT = "207"
TV_CAT = "208"
TRACKERS = (
    "&tr=udp://tracker.opentrackr.org:1337/announce"
    "&tr=udp://open.stealth.si:80/announce"
    "&tr=udp://tracker.torrent.eu.org:451/announce"
)

def get_url(**kwargs):
    return "{0}?{1}".format(URL, urllib.parse.urlencode(kwargs))

def parse_params(param_string):
    params = {}
    if param_string:
        if param_string.startswith("?"):
            param_string = param_string[1:]
        for part in param_string.split("&"):
            if "=" in part:
                k, v = part.split("=", 1)
                params[k] = urllib.parse.unquote(v)
    return params

def fetch_json(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        xbmc.log("[OCP] API fetch error: %s" % str(e), xbmc.LOGERROR)
        return []

def fetch_html(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8-sig")
    except Exception as e:
        xbmc.log("[OCP] HTML fetch error: %s" % str(e), xbmc.LOGERROR)
        return ""

def parse_tpb_html(html):
    results = []
    rows = re.findall(r'<div class="detName">.*?</td>\s*</tr>', html, re.DOTALL)
    for row in rows:
        name_m = re.search(r'class="detLink"[^>]*>(.*?)</a>', row)
        magnet_m = re.search(r'href="(magnet:\?[^"]+)"', row)
        seeds_m = re.findall(r'<td[^>]*>(\d+)</td>', row)
        size_m = re.search(r'Size (\S+)', row)
        
        if name_m and magnet_m:
            magnet = magnet_m.group(1)
            hash_m = re.search(r'btih:([a-fA-F0-9]+)', magnet)
            info_hash = hash_m.group(1).upper() if hash_m else ""
            
            results.append({
                "info_hash": info_hash,
                "name": name_m.group(1),
                "seeders": int(seeds_m[0]) if len(seeds_m) > 0 else 0,
                "leechers": int(seeds_m[1]) if len(seeds_m) > 1 else 0,
                "size": size_m.group(1).replace("&nbsp;", " ") if size_m else "Unknown",
                "source": "TPB"
            })
    return results

def parse_kickass_search(html):
    results = []
    links = re.findall(r'<a[^>]*href="(/[^"]+\.html)"[^>]*class="cellMainLink"[^>]*>(.*?)</a>', html, re.DOTALL)
    sizes = re.findall(r'<td[^>]*>\s*([\d.]+\s*(?:GiB|MiB|GB|MB|KB))\s*</td>', html)
    seeds_list = re.findall(r'<td[^>]*>\s*(\d+)\s*</td>', html)
    
    for i, (link, name) in enumerate(links):
        clean_name = re.sub(r'<[^>]+>', '', name).strip()
        if not clean_name:
            continue
            
        size = sizes[i] if i < len(sizes) else "Unknown"
        seed_idx = i * 2
        seeders = int(seeds_list[seed_idx]) if seed_idx < len(seeds_list) else 0
        leechers = int(seeds_list[seed_idx + 1]) if seed_idx + 1 < len(seeds_list) else 0
        
        results.append({
            "info_hash": "",
            "name": clean_name,
            "seeders": seeders,
            "leechers": leechers,
            "size": size,
            "source": "KickAss",
            "detail_url": KICKASS_BASE + link
        })
    return results

def fetch_kickass_magnet(detail_url):
    html = fetch_html(detail_url)
    if html:
        magnets = re.findall(r'href="(magnet:\?[^"]+)"', html)
        if magnets:
            magnet = magnets[0]
            hash_m = re.search(r'btih:([a-fA-F0-9]+)', magnet)
            return {
                "info_hash": hash_m.group(1).upper() if hash_m else "",
                "magnet": magnet
            }
    return None

def fetch_kickass_magnets_parallel(ka_results, max_items=10):
    results = []
    threads = []
    
    def fetch_and_store(item):
        magnet_data = fetch_kickass_magnet(item.get("detail_url", ""))
        if magnet_data:
            item["info_hash"] = magnet_data["info_hash"]
            item["magnet"] = magnet_data["magnet"]
            results.append(item)
    
    for item in ka_results[:max_items]:
        t = threading.Thread(target=fetch_and_store, args=(item,))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join(timeout=10)
    
    return results

def set_fanart():
    """Set the addon fanart as the background for all windows"""
    xbmcgui.Window(HANDLE).setProperty('Fanart_Image', FANART_PATH)

def merge_and_display(api_data, tpb_data, ka_data):
    seen = {}
    merged = []
    
    for item in (api_data or []):
        h = item.get("info_hash", "").upper()
        if h and h not in seen:
            seen[h] = True
            item["source"] = "API"
            merged.append(item)
    
    for item in (tpb_data or []):
        h = item.get("info_hash", "").upper()
        if h and h not in seen:
            seen[h] = True
            merged.append(item)
    
    for item in (ka_data or []):
        merged.append(item)
    
    merged.sort(key=lambda x: int(x.get("seeders", 0)), reverse=True)
    
    for item in merged:
        if len(item.get("info_hash", "")) != 40:
            continue
            
        h = item["info_hash"].upper()
        n = item.get("name", "Unknown")
        magnet = item.get("magnet", "")
        
        if not magnet:
            magnet = "magnet:?xt=urn:btih:{0}&dn={1}{2}".format(h, urllib.parse.quote(n), TRACKERS)
        
        source = item.get("source", "")
        label = "{0} [{1}][S:{2} L:{3} - {4}]".format(n[:70], source, item.get("seeders", 0), item.get("leechers", 0), item.get("size", "?"))
        
        li = xbmcgui.ListItem(label=label)
        li.setInfo("video", {"title": n})
        li.setProperty("IsPlayable", "true")
        li.setArt({"icon": "DefaultVideo.png", "fanart": FANART_PATH})
        xbmcplugin.addDirectoryItem(HANDLE, get_url(action="play", magnet=magnet, name=n, detail_url=item.get("detail_url", "")), li, isFolder=False)

def fetch_all_sources(query, cat, num_pages=5):
    """Fetch from all sources in parallel across multiple pages"""
    all_api = []
    all_tpb = []
    all_ka = []
    
    def fetch_api_page(page):
        url = "{0}/q.php?q={1}&cat={2}&p={3}".format(API_BASE, urllib.parse.quote(query), cat, page)
        data = fetch_json(url)
        if data:
            all_api.extend(data)
    
    def fetch_tpb_page(page):
        url = "{0}/search/{1}/{2}/7/{3}".format(TPB_BASE, urllib.parse.quote(query), page, cat)
        html = fetch_html(url)
        if html:
            all_tpb.extend(parse_tpb_html(html))
    
    def fetch_kickass_page(page):
        url = "{0}/search/{1}".format(KICKASS_BASE, urllib.parse.quote(query))
        html = fetch_html(url)
        if html:
            all_ka.extend(parse_kickass_search(html))
    
    threads = []
    
    # Fetch API pages in parallel
    for page in range(num_pages):
        t = threading.Thread(target=fetch_api_page, args=(page,))
        t.start()
        threads.append(t)
    
    # Fetch TPB pages in parallel
    for page in range(num_pages):
        t = threading.Thread(target=fetch_tpb_page, args=(page,))
        t.start()
        threads.append(t)
    
    # Fetch KickAss (only first page since it's slower)
    t = threading.Thread(target=fetch_kickass_page, args=(0,))
    t.start()
    threads.append(t)
    
    # Wait for all threads
    for t in threads:
        t.join(timeout=20)
    
    # Fetch KickAss magnets in parallel
    if all_ka:
        return all_api, all_tpb, fetch_kickass_magnets_parallel(all_ka, max_items=15)
    
    return all_api, all_tpb, all_ka

def do_search(cat, query, search_type):
    set_fanart()
    if not query:
        kb = xbmc.Keyboard("", "Search {0}...".format(search_type))
        kb.doModal()
        if kb.isConfirmed() and kb.getText():
            query = kb.getText().strip()
        else:
            xbmcplugin.endOfDirectory(HANDLE)
            return
    
    progress = xbmcgui.DialogProgress()
    progress.create("Open Code Player", "Searching multiple pages...")
    
    api_data, tpb_data, ka_data = fetch_all_sources(query, cat, num_pages=5)
    progress.close()
    
    merge_and_display(api_data, tpb_data, ka_data)
    xbmcplugin.endOfDirectory(HANDLE)

def do_trending(cat, query, label):
    set_fanart()
    progress = xbmcgui.DialogProgress()
    progress.create("Open Code Player", "Loading {0}...".format(label))
    
    api_data, tpb_data, ka_data = fetch_all_sources(query, cat, num_pages=5)
    progress.close()
    
    merge_and_display(api_data, tpb_data, ka_data)
    xbmcplugin.endOfDirectory(HANDLE)

def play_magnet(magnet, name, detail_url):
    if not magnet:
        xbmcplugin.endOfDirectory(HANDLE)
        return
    
    if detail_url and "btih" not in magnet:
        progress = xbmcgui.DialogProgress()
        progress.create("Open Code Player", "Getting magnet link...")
        magnet_data = fetch_kickass_magnet(detail_url)
        progress.close()
        if magnet_data:
            magnet = magnet_data["magnet"]
    
    play_url = "plugin://plugin.video.torrest/play_magnet?magnet={0}".format(urllib.parse.quote(magnet))
    xbmc.log("[OCP] Playing: {0}".format(play_url), xbmc.LOGINFO)
    xbmc.executebuiltin("PlayMedia({0})".format(play_url))
    xbmcplugin.endOfDirectory(HANDLE)

def show_menu():
    set_fanart()
    items = [
        ("[B][COLOR=orange]Search Movies[/COLOR][/B]", "search_movies", "DefaultFolder.png"),
        ("[B][COLOR=gold]Trending Movies[/COLOR][/B]", "trending_movies", "DefaultMovies.png"),
        ("[B][COLOR=blue]Search TV Shows[/COLOR][/B]", "search_tv", "DefaultTVShows.png"),
        ("[B][COLOR=skyblue]Trending TV Shows[/COLOR][/B]", "trending_tv", "DefaultTVShows.png")
    ]
    for label, action, icon in items:
        li = xbmcgui.ListItem(label)
        li.setArt({"icon": icon, "fanart": FANART_PATH})
        xbmcplugin.addDirectoryItem(HANDLE, get_url(action=action), li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)

def main():
    try:
        set_fanart()
        p = parse_params(PARAMS)
        a = p.get("action", "")
        
        if a == "search_movies" or a == "do_search":
            do_search(int(p.get("cat", MOVIE_CAT)), p.get("query"), p.get("search_type", "movies"))
        elif a == "search_tv":
            do_search(TV_CAT, p.get("query"), "TV shows")
        elif a == "trending_movies" or a == "do_trending":
            do_trending(int(p.get("cat", MOVIE_CAT)), p.get("query"), p.get("label", "trending movies"))
        elif a == "trending_tv":
            do_trending(TV_CAT, "S01E01", "trending TV shows")
        elif a == "play":
            play_magnet(p.get("magnet"), p.get("name"), p.get("detail_url"))
        else:
            show_menu()
    except Exception as e:
        xbmc.log("[OCP] CRASH: %s" % str(e), xbmc.LOGFATAL)
        xbmcgui.Dialog().ok("Error", str(e))
        xbmcplugin.endOfDirectory(HANDLE)

if __name__ == "__main__":
    main()
