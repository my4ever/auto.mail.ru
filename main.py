import requests
import json
from time import sleep
from random import randint
from collections import OrderedDict
from bs4 import BeautifulSoup as bs

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}


def get_source(url):
    """
    Getting a source HTML file.
    """
    scr = requests.get(url, headers=headers)
    with open('source.html', 'w') as file:
        file.write(scr.text)


def get_data():
    """
    Getting data out html code.
    """
    brands = {}
    # Opening html code.
    with open('source.html', 'r') as file:
        source_data = file.read()
    # Getting brands.
    soup = bs(source_data, 'lxml')
    all_auto_brands = soup.findAll('div', class_='cols__column cols__column_small_percent-33 cols__column_medium_percent-33 cols__column_large_percent-25 margin_top_20')

    for brand in all_auto_brands[0]:
        sleep(randint(1, 2))
        if brand.txt not in brands:
            link = 'https://auto.mail.ru' + brand.find('a', class_='p-firm__text link-holder').get('href')
            brands[brand.text] = get_models(link)

    save_data(OrderedDict(sorted(brands.items())))  # Ordering data by keys before sending it to save


def get_models(url):
    """
    Getting all models for a brand.
    """
    get_source(url)
    models = []
    # Opening HTML code.
    with open('source.html') as file:
        source_data = file.read()
    # Getting models.
    soup = bs(source_data, 'lxml')
    all_models = soup.findAll('a', class_='p-car__title link-holder')
    for model in all_models:
        models.append(model.text)

    return sorted(models)


def save_data(data):
    """
    Dumping data into json file.
    """
    with open('cars.json', 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    get_source('https://auto.mail.ru/catalog/')
    get_data()
