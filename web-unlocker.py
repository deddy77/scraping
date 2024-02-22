import sys
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import urllib.request

url ="https://codeavecjonathan.com/scraping/techsport/"

opener = urllib.request.build_opener(
    urllib.request.ProxyHandler(
        {'http': 'http://brd-customer-hl_4640318e-zone-web_unlocker1:ga4qyg9pcdzd@brd.superproxy.io:22225',
        'https': 'http://brd-customer-hl_4640318e-zone-web_unlocker1:ga4qyg9pcdzd@brd.superproxy.io:22225'}))
html = opener.open(url).read().decode("ISO-8859-1")

with open('web-unlocker.html', 'w', encoding='utf-8') as f:
    f.write(html)

f.close()
print("END")