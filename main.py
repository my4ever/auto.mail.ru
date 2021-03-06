import json
import os

import requests
from time import sleep
from random import randint
from collections import OrderedDict
from bs4 import BeautifulSoup as bs

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}


def get_source(url):
    """
    Getting a source HTML code,
    and putting it into created directory temp.
    """
    os.makedirs('temp', exist_ok=True)
    html_code = requests.get(url, headers=headers)
    with open('temp/source.html', 'w') as file:
        file.write(html_code.text)


def open_html():
    """
    Opening HTML code.
    """
    with open('temp/source.html') as file:
        source_data = file.read()
    return source_data


def get_data():
    """
    Getting data out html code.
    """
    brands = dict()
    source_data = open_html()
    # Getting brands.
    soup = bs(source_data, 'lxml')
    all_auto_brands = soup.findAll('div', class_='cols__column '
                                                 'cols__column_small_percent-33 '
                                                 'cols__column_medium_percent-33 '
                                                 'cols__column_large_percent-25 '
                                                 'margin_top_20')

    for brand in all_auto_brands[1]:
        sleep(randint(1, 2))
        if brand.txt not in brands:
            link = 'https://auto.mail.ru' + brand.find('a', class_='p-firm__text '
                                                                   'link-holder').get('href')
            # Getting models of a brand.
            brands[brand.text] = get_models(link)

    return OrderedDict(sorted(brands.items()))  # Ordering data by keys before sending it to save


def get_models(url):
    """
    Getting all models for a brand.
    """
    get_source(url)
    models = list()
    source_data = open_html()
    # Getting models.
    soup = bs(source_data, 'lxml')
    all_models = soup.findAll('a', class_='p-car__title link-holder')
    for model in all_models:
        models.append(model.text)

    return sorted(models)


def save_data(data):
    """
    Creating directory result,
    dumping data into json file into it,
    removing temp directory and file in it.
    """
    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'temp/source.html')
    dir_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'temp')

    os.makedirs('result', exist_ok=True)

    with open('result/cars.json', 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    os.remove(file_path)
    os.rmdir(dir_path)

if __name__ == '__main__':
    get_source('https://auto.mail.ru/catalog/')
    save_data(get_data())
