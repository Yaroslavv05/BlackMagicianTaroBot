import requests
from bs4 import BeautifulSoup as BS


class Parser_card_day:

    def parser_text(self):
        for i in range(1, 78):
            url = f'https://taro.lv/ru/78_dverej/door_{i+1}'
            respons = requests.get(url)
            soup = BS(respons.content, 'html.parser')
            text = soup.find('div', {'class': 'accordion-item-content-wrap'}).text
            name_card = soup.find('div', {'class': 'relative-position'}).text.split('\n')
            with open(f'static/txt/{name_card[1]}.txt', 'a', encoding='utf8') as file:
                file.write(text)

    def parser_img(self):
        for i in range(1, 78):
            url = f'https://taro.lv/ru/78_dverej/door_{i+1}'
            respons = requests.get(url)
            soup = BS(respons.content, 'html.parser')
            name_card = soup.find('div', {'class': 'relative-position'}).text.split('\n')
            img = soup.find('div', {'class': 'card-image'})
            img_url = img.find('img').attrs.get('src')
            url2 = f'https://taro.lv{img_url}'
            image_date = requests.get(url2, verify=False).content
            with open(f'static/img/{name_card[1]}.jpg', 'wb') as handler:
                handler.write(image_date)


do = Parser_card_day()
do.parser_text()
do.parser_img()


class Parser_card_love:

    def parser_txt(self):
        for i in range(1, 78):
            url = f'https://taro.lv/ru/78_dverej/door_{i}'
            respons = requests.get(url)
            soup = BS(respons.content, 'html.parser')
            text_love = soup.find_all('div', {'class': 'wysiwyg'})[6].text
            name_card = soup.find('div', {'class': 'relative-position'}).text.split('\n')[1]
            with open(f'static/txt_love/{name_card}.txt', 'a', encoding='utf8') as file:
                file.write(text_love)


do_love = Parser_card_love()
do_love.parser_txt()