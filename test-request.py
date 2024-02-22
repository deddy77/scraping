import requests
from bs4 import BeautifulSoup



#url


url = "https://ww.amazon.com/"

HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"} 

response = requests.get(url, headers=HEADERS)
response.encoding = "ISO-8859-1"#response.apparent_encoding


if response.status_code == 200:
    print("Tout s'est bien passé")
    html = response.text
    #print(html)
    f = open("test-request.html", "w")
    f.write(html)
    f.close()



else:
    print("Problème de requête: ", response.status_code)




print("END")