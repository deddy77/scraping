import requests
from bs4 import BeautifulSoup




url = "https://codeavecjonathan.com/scraping/recette_js"

HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"} 

def get_text_if_not_none(e):
    if e is not None:
        return e.text.strip()
    return None


response = requests.get(url, headers=HEADERS)
response.encoding = "ISO-8859-1"


if response.status_code == 200:
    print("Tout s'est bien passé")
    html = response.text
    #print(html)
    f = open("recette.html", "w")
    f.write(html)
    f.close()

    soup = BeautifulSoup(html, "html5lib")

    titre = soup.find("h1").text
    print(titre)
    description = get_text_if_not_none(soup.find("p", class_="description"))
    print(description)

    # Ingrédients
    div_ingredients = soup.find("div", class_="ingredients")

    e_ingredients = div_ingredients.find_all("p")
    for e_ingredient in e_ingredients:
        print("Ingrédient: ", e_ingredient.text.strip())

    t_preparation = soup.find("table", class_="preparation")
    step_preparations = t_preparation.find_all("td", class_="preparation_etape")
    for step_prepatation in step_preparations:
        print("Etape: ", step_prepatation.text.strip() )















else:
    print("Problème de requête: ", response.status_code)


response = requests.get(url)

print("END")