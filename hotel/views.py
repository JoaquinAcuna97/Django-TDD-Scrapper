from django.shortcuts import render


# Create your views here.


def get_html_data(url):
    import requests
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html = session.get(url).text
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())
    return soup


def get_hotel_from_html_soup(url, soup):
    # Nombre del hotel
    nombre = soup.find(id="hp_hotel_name")
    print(f'Nombre: {nombre.text}')

    # Dirección
    dire = soup.find("span", class_="hp_address_subtitle")
    print(f'Dirección: {dire.text}')


# URL de las 5 principales fotos del hotel
    pictures = soup.find("span", class_="hp_address_subtitle")
    pictures_link = pictures.find_all_next("a", class_='bh-photo-grid-thumb')
    for pic in pictures_link:
        print(f'FOTOS: {pic["href"]}')

# Para cada tipo de habitación del hotel:
    rooms_table = soup.find_all('table', class_='room-info')
    for room in rooms_table:
        room_link = pictures.find_all("a", class_='togglelink')
# Nombre
        nombre = room_link['data-room-name-en']
        print(f'Cuarto con Nombre: {nombre}')
        room_html = get_html_data(url+"#"+room_link)
# Tamaño de la habitación
        room_size = room_html.select('p[data-name-en="roomsize"]').next_sibling
        print(f'    SIZE: {room_size.text}')
# URL de las 5 principales fotos del tipo de habitación
        room_pictures = room_html.find('div', class_='b_nha_hotel_small_images')
        pictures_link = room_pictures.find_all_next('img')
        for pic in pictures_link:
            print(f'FOTOS: {pic["src"]}')
            print(f'    FOTOS: {pic["src"]}')

# Listado completo de amenities y equipamiento de la habitación


# Calificación del hotel y cantidad de reviews recibidos
    calif = soup.find("div", class_="bui-review-score__badge")
    print(f'Calificación del hotel: {calif.text}')
    revi = soup.find("div", class_="bui-review-score__text")
    print(f'Cantidad de reviews recibidos: {revi.text}')


def home_page(request):
    if 'url' in request.GET:
        url = request.GET.get('url')
        html_data = get_html_data(url)
        get_hotel_from_html_soup(url, html_data)
        # fetch the data from booking.com

    return render(request, 'hotel/home.html')
