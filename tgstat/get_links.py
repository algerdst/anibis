import time
from links import a

import requests
import datetime
import sqlite3
from bs4 import BeautifulSoup
import re

db = sqlite3.connect('tg_channels.db')
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS tg_channels_info (
    name varchar(500),
    description text,
    subscribers varchar(50),
    subscribers_change varchar(50),
    img text,
    link varchar(500),
    status varchar(10),
    category varchar(500),
    is_selling varchar DEFAULT Нет
    
)""")
db.commit()

tg_links = sql.execute("""SELECT DISTINCT link, category
    FROM tg_channels_links 
""").fetchall()
links_dict={}
for i in tg_links:
    links_dict[i[0]]=i[1]
for i in a:
    if i in links_dict:
        del links_dict[i]
tg_links=[(i, links_dict[i]) for i in links_dict]
links_dict.clear()
count_links=len(tg_links)
pattern = r'=(.*)'

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
count=0
for link in tg_links:
    category = link[1]
    url = link[0]
    print(url)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    channel_wrapper = soup.find('div', class_='tg-channel-wrapper')
    channel_name = channel_wrapper.find('h1').text.replace("'",'')
    status = channel_wrapper.find('span', class_='tg-options-public')
    if status:
        status = 'Публичный'
    else:
        status = 'Приватный'
    channel_link = channel_wrapper.find('h1').find('a')['href']
    channel_link = re.findall(pattern, channel_link)[0]
    if status == 'Приватный':
        channel_link = 'tg://join?invite=' + channel_link
    else:
        channel_link = 'https://t.me/' + channel_link
    is_selling = channel_wrapper.find('span', 'tg-options-sale')
    if is_selling:
        is_selling = 'Да'
    else:
        is_selling = 'Нет'
    description = channel_wrapper.find('div', class_='tg-channel-description').text.replace("'",'')
    img = channel_wrapper.find('div', 'tg-channel-img').find('img')['src']
    subscribers = channel_wrapper.find('span', 'tg-user-count').text
    try:
        subscribers_change = channel_wrapper.find('span', 'tg-user-change').text
    except:
        subscribers_change=''
    sql.execute(f"""INSERT INTO tg_channels_info (name,description, subscribers, subscribers_change, img, link,status,
                    category, is_selling)
                    VALUES ('{channel_name}','{description}','{subscribers}','{subscribers_change}','{img}','{channel_link}','{status}','{category}','{is_selling}')""")
    db.commit()
    time.sleep(2)
    count+=1

    print(f"Собрано ссылок - {count}. Осталось собрать {count_links-count}")
