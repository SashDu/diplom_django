from bs4 import BeautifulSoup  # Для парсинга HTML
from selenium import webdriver  # Для создания своего браузера
from selenium.webdriver.chrome.service import Service  # Для настройки Chrome
from time import sleep

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
options_chrome = webdriver.ChromeOptions()  # Настройки браузера
options_chrome.add_argument('headless')  # Настройки браузера (без визуального окна)
service = Service(executable_path="driver_chrome/chromedriver.exe")  # Настройки браузера
browser = webdriver.Chrome(service=service, options=options_chrome)  # Запуск браузера


class Rating:
    @staticmethod
    def get_rows():
        url = 'https://markakachestva.ru/best-brands/2808-luchshie-internet-magaziny-sportivnyh-tovarov.html'
        browser.get(url)  # Открытие страницы с url
        sleep(1)
        soup = BeautifulSoup(browser.page_source, 'lxml')  # Создание обертки
        table_rating = soup.find("table", class_="tableRating")  # вся нужная таблица
        results = [[], [], [],]
        position_row = table_rating.find("tbody").find_all("tr")
        for i in position_row:
            manufacturer = i.find_all("td")[1].text.strip()
            rating = i.find_all("td")[2].text.strip()
            rating_pr = i.find_all("td")[3].text.strip()
            results[1].append(manufacturer)
            results[2].append(rating)
            results[3].append(rating_pr)
        return results

    @staticmethod
    # часть для получения названий колонок
    def get_cols():
        url = 'https://markakachestva.ru/best-brands/2808-luchshie-internet-magaziny-sportivnyh-tovarov.html'
        browser.get(url)  # Открытие страницы с url
        sleep(1)
        soup = BeautifulSoup(browser.page_source, 'lxml')  # Создание обертки
        table_rating = soup.find("table", class_="tableRating")  # вся нужная таблица
        result = []
        position_col = table_rating.find_all('span', class_="innerText")[:2]  # первая строка c колонками
        for i in position_col:
            title = i.text  # получили нужные названия колонок
            result.append(title)
        return result


obj = Rating()  # экземпляр класса
# print(obj.get_rows())
# print(obj.get_cols())
