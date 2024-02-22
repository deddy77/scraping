import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from datetime import datetime
import json
from openai import OpenAI

SBR_WS_CDP = 'your scraping browser websocket url here'

URLS = [
]

# Chemin du fichier JSON pour le stockage des données
JSON_DATA_FILE = "techsport-gpt.json"

# Obtenir la date du jour pour les enregistrements
DATE_TODAY = datetime.today()
DATE_TODAY_STR = DATE_TODAY.strftime("%Y-%m-%d")


# Clé API OPENAI
OPENAI_KEY = "your_openai_key_here"

# Initialiser le client OpenAI
openai_client = OpenAI(api_key=OPENAI_KEY)


# Fonction pour obtenir la complétion à partir d'OpenAI
def get_completion(prompt, model="gpt-3.5-turbo", temperature=0.7):
    messages = [{"role": "user", "content": prompt}]
    chat_completion = openai_client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return chat_completion.choices[0].message.content


# Variable pour activer/désactiver le contournement du scraping
BYPASS_SCRAPING = False


# Fonction pour obtenir le texte si non nul
def get_text_if_not_none(e):
    if e is not None:
        return e.text.strip()
    return None


# Fonction pour extraire les informations de la page du produit
def extract_product_page_infos(html):
    infos = {}

    bs = BeautifulSoup(html, 'html.parser')

    # Extraire le titre
    infos["title"] = get_text_if_not_none(bs.find("span", id="productTitle"))

    # Extraire le nombre de notes
    rating_text = get_text_if_not_none(bs.find("span", id="customer-review-text"))
    infos["nb_ratings"] = int(rating_text.split()[0]) if rating_text else 0

    # Extraire le prix
    price_whole = get_text_if_not_none(bs.find("span", class_="price-whole"))
    price_fraction = get_text_if_not_none(bs.find("span", class_="price-fraction"))
    price = float(price_whole + "." + price_fraction) if price_whole and price_fraction else None
    infos["price"] = price

    # Extraire la description
    description = get_text_if_not_none(bs.find("div", id="product-description"))
    infos["description"] = description

    return infos


# Fonction principale pour exécuter le script
async def run(pw):
    # Stockage des données
    all_data = {}

    # Charger les données existantes depuis le fichier JSON
    try:
        with open(JSON_DATA_FILE, "r") as json_file:
            all_data = json.load(json_file)
    except FileNotFoundError:
        print("No JSON data file found")

    # Se connecter au navigateur de scraping
    if not BYPASS_SCRAPING:
        print('Connecting to Scraping Browser...')
        browser = await pw.chromium.connect_over_cdp(SBR_WS_CDP)

    try:
        # Parcourir les URLs
        for i, url in enumerate(URLS, start=1):
            print(f'Processing URL {i} of {len(URLS)}: {url}...')
            if not BYPASS_SCRAPING:
                page = await browser.new_page()
                print('Connected! Navigating...')
                await page.goto(url)
                await page.screenshot(path=f'./scraping-browser-{i}.png', full_page=True)
                print('Screenshot taken! Navigating...')
                print('Navigated! Scraping page content...')
                html = await page.content()
                
                # Save the HTML content to a file
                with open(f'./scriping-browser{i}.html', 'w', encoding='utf-8') as f:
                    f.write(html)

                f.close()
                print("HTML content saved to file.")

                # Extraire les informations de la page
                infos = extract_product_page_infos(html)
                print('Extracted infos:', infos)

                # Vérifier si l'URL existe déjà dans les données
                if url not in all_data:
                    all_data[url] = {"title": infos["title"], "description": infos["description"], "records": {}}

                # Vérifier si le prix est présent dans les informations extraites
                if 'price' in infos:
                    all_data[url]["records"][DATE_TODAY_STR] = {"price": infos['price'], "nb_ratings": infos["nb_ratings"]}
                else:
                    # Gérer le cas où le prix n'est pas présent
                    all_data[url]["records"][DATE_TODAY_STR] = {"price": None, "nb_ratings": infos["nb_ratings"]}

    finally:
        if not BYPASS_SCRAPING:
            await browser.close()
            print(f'End of scraping for {url}')

        # Enregistrer les données dans le fichier JSON
        with open(JSON_DATA_FILE, "w") as json_file:
            json.dump(all_data, json_file)


# Fonction principale pour exécuter l'application asynchrone
async def main():
    async with async_playwright() as playwright:
        await run(playwright)


# Point d'entrée de l'application
if __name__ == '__main__':
    asyncio.run(main())
