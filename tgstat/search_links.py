import time

import requests
import datetime
import sqlite3
from bs4 import BeautifulSoup


def get_categories():
    headers = {
        'authority': 'tgramsearch.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru,en;q=0.9',
        'cookie': 'uiso=BY; uip=37.215.26.65; _ym_uid=1709912784937583147; _ym_d=1709912784; _ym_isad=2; _ym_visorc=b; adstgid=%5B1%5D; adstgid=%5B1%2C0%5D',
        'referer': 'https://tgramsearch.com/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "YaBrowser";v="24.1", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'
    }
    response = requests.get('https://tgramsearch.com/', headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    cats = soup.find('ul', 'tg-categories').find_all('li')
    categories = []
    for cat in cats:
        link = 'https://tgramsearch.com' + cat.find('a')['href']
        categories.append(link)
    return categories


count = 0
db = sqlite3.connect('tg_channels.db')
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS tg_channels_links (
    link varchar(500),
    category varchar(500)
)""")
db.commit()

# proxies={
#         'http': f"http://{user}:{password}@{host}:{port}",
#         'https': f"http://{user}:{password}@{host}:{port}",
#     }
for url in get_categories():
    headers = {
        'authority': 'tgramsearch.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru,en;q=0.9',
        'cookie': 'uiso=BY; uip=37.215.26.65; _ym_uid=1709912784937583147; _ym_d=1709912784; _ym_isad=2; _ym_visorc=b; adstgid=%5B1%5D; adstgid=%5B1%2C0%5D',
        'referer': 'https://tgramsearch.com/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "YaBrowser";v="24.1", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'
    }
    response = requests.request("GET", url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    pages = int(soup.findAll('li', 'tg-pager-li')[-1].text)
    for page in range(1, pages + 1):
        if page == 1:
            soup = soup
        else:
            response = requests.request("GET", f"{url}?page={page}", headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
        if response.status_code != 200:
            print(f'Ошибка статус кода {response.status_code}')
            break
        blocks = soup.findAll('div', 'tg-channel-wrapper')
        category = soup.find('h1').text.replace('Телеграм каналы в категории', '').replace('«', '').replace('»',
                                                                                                            '').strip()
        for block in blocks:
            link_text = block.find('div', class_='tg-channel-link').find('a').text
            if link_text == 'OnlyFan$ лучшее' or link_text == 'Телеграм сливы':
                continue
            else:
                link = 'https://tgramsearch.com' + block.find('div', class_='tg-channel-link').find('a')['href']
                sql.execute(f"""INSERT INTO tg_channels_links (link,category)
                                    VALUES ('{link}','{category}')
                                    """)
                db.commit()
        print(f'Обработал страницу {page} в категории {category}')
        time.sleep(5)
