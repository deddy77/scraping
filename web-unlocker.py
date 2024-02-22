import sys
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import urllib.request

#url =

opener = urllib.request.build_opener(
    urllib.request.ProxyHandler(
        {'http': 'your_proxy_here'})),
        'https': 'your_proxy_here'}))
html = opener.open(url).read().decode("ISO-8859-1")

with open('web-unlocker.html', 'w', encoding='utf-8') as f:
    f.write(html)

f.close()
print("END")