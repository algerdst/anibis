import csv
import time

import requests
from seleniumbase import SB
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from categories import categories_urls


category_index=0
page_index=1
gotted_links=[]
gotted_phones=[]


with open('отработанные ссылки.txt','r',encoding='utf-8') as file:
    for i in file:
        gotted_links.append(i.replace('\n',''))

with open('отработанные номера телефонов.txt','r',encoding='utf-8') as file:
    for i in file:
        gotted_phones.append(i.replace('\n',''))
while True:
    break_flag = False
    with SB(uc=True) as sb:
        sb.open('https://www.anibis.ch/fr/start/login')
        time.sleep(5)
        try:
            sb.find_element(By.ID, 'onetrust-accept-btn-handler').click()
            login_field=sb.find_elements(By.CSS_SELECTOR, 'input.MuiInputBase-input')[0]
            password_field=sb.find_elements(By.CSS_SELECTOR, 'input.MuiInputBase-input')[1]
            submit=sb.find_element(By.CSS_SELECTOR, 'button.MuiButtonBase-root')
            login_field.send_keys('Topassure@gmail.com')
            password_field.send_keys('Sasd$%hsh554gs#')
            submit.click()
            time.sleep(3)
        except:
            continue
        while category_index<len(categories_urls):
            if break_flag is True:
                break
            url=categories_urls[category_index]
            url=f"{url}page={page_index}"
            sb.open(url)
            source = sb.get_page_source()
            soup = BeautifulSoup(source, 'lxml')
            links = soup.find_all('a', class_='mui-style-blugjv')
            max_page=soup.find('ul', class_='mui-style-nhb8h9').findAll('li')[-2].text
            max_page=int(max_page)
            link_index = 0
            while link_index<30:
                try:
                    link = 'https://www.anibis.ch'+links[link_index]['href']
                except:
                    category_index+=1
                    break
                if link in gotted_links:
                    link_index+=1
                    continue
                sb.open(link)
                try:
                    sb.click('button:contains("Voir numéro")')
                    source = sb.get_page_source()
                    soup = BeautifulSoup(source, 'lxml')
                    number = soup.find('div', class_='ItemContact_sellerCard__f_Wiq').find('div',
                                                                               class_='mui-style-8uhtka').text
                    if number == "Voir numéro":
                        break_flag=True
                        break
                    print(number)
                    print('page '+page_index)
                    print(link)
                    print()
                    number = "'" + number + "'"
                    if number not in gotted_phones:
                        with open('result.csv', 'a', newline='', encoding='utf-8-sig') as file:
                            writer=csv.writer(file, delimiter=';')
                            writer.writerow([number])
                    with open('отработанные номера телефонов.txt', 'a', encoding='utf-8') as file:
                        file.write(number+'\n')
                    gotted_phones.append(number)
                    link_index+=1

                    with open('отработанные ссылки.txt', 'a', encoding='utf-8') as file:
                        file.write(link+'\n')
                    gotted_links.append(link)


                except:
                    with open('отработанные ссылки.txt', 'a', encoding='utf-8') as file:
                        file.write(link+'\n')
                    gotted_links.append(link)
                    link_index += 1
                    continue
            else:
                if page_index<=max_page:
                    page_index+=1
                    continue
                else:
                    category_index+=1
                    page_index=1
                    continue
