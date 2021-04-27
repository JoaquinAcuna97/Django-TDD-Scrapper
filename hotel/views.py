from django.shortcuts import render
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import requests
import time
from bs4 import BeautifulSoup
import os

# Create your views here.


def get_rendered_html_data(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.set_page_load_timeout(100)
    driver.get(url)
    time.sleep(15)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return soup


def get_html_data(url):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html = session.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_hotel_from_html_soup(url, soup):
    hotel = {}
    # Nombre del hotel
    name = soup.find(id="hp_hotel_name")
    hotel['name'] = name.text

    # Dirección
    address = soup.find("span", class_="hp_address_subtitle")
    hotel['address'] = address.text

    # URL de las 5 principales fotos del hotel
    pictures = soup.find("span", class_="hp_address_subtitle")
    pictures_link = pictures.find_all_next("a", class_='bh-photo-grid-thumb')
    hotel['pictures'] = []
    for pic in pictures_link:
        hotel['pictures'].append(pic["href"])

    # Para cada tipo de habitación del hotel:
    rooms_table = soup.find_all('div', class_='room-info')
    hotel['rooms'] = []
    for room in rooms_table:
        dic_room = {}
        room_link = room.find("a", class_='togglelink')

        # Nombre
        name = room_link['data-room-name-en']
        dic_room['name']= name
        room_html = get_rendered_html_data(url + room_link['href'].replace('RD', 'room_'))

        # Tamaño de la habitación
        room_size = room_html.find('p', attrs={'data-name-en': "roomsize"})
        if room_size:
            room_size = room_size.next_sibling
            if room_size:
                room_size = room_size.next_sibling
        dic_room['size'] = room_size

        # URL de las 5 principales fotos del tipo de habitación
        room_pictures = room_html.find('div', class_='slick-track')
        if room_pictures:
            pictures_link = room_pictures.find_all_next('img', limit=5)
            dic_room['pictures'] = []
            for pic in pictures_link:
                if 'src' in pic.attrs:
                    dic_room['pictures'].append(pic["src"])
                elif 'data-lazy' in pic.attrs:
                    dic_room['pictures'].append(pic["data-lazy"])
            hotel['rooms'].append(dic_room)


    # Listado completo de amenities y equipamiento de la habitación
    # pending

    # Calificación del hotel y cantidad de reviews recibidos
    score = soup.find("div", class_="bui-review-score__badge")
    hotel['score'] = score.text
    review = soup.find("div", class_="bui-review-score__text")
    hotel['review'] = review.text

    return hotel


def home_page(request):
    hotel = None
    if 'url' in request.GET:
        url = request.GET.get('url')
        html_data = get_html_data(url)
        hotel = get_hotel_from_html_soup(url, html_data)
        print(hotel)
        # fetch the data from booking.com
    return render(request, 'hotel/home.html', {'hotel':hotel})
