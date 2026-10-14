import urllib.request
import re

url = "https://www.youtube.com/watch?v=f6ArFvSPlkw"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    cids = set(re.findall(r'"channelId":"([^"]+)"', html))
    print("Found channel IDs on watch page:", cids)
    names = set(re.findall(r'"ownerChannelName":"([^"]+)"', html))
    print("Owner channel name:", names)
