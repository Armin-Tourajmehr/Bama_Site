import bama_backend
import requests
from bs4 import BeautifulSoup
import re


def bama_link():
    # Get data from bama
    bama = requests.get('https://bama.ir/')
    soup = BeautifulSoup(bama.text, 'html.parser')
    url = soup.find_all('a', attrs={'id': 'carTaga'})[1].get('href')
    buy_car(url)


def buy_car(url):
    # link of buy_car
    url_sellCar = requests.get('https://bama.ir/' + url)
    soup_2 = BeautifulSoup(url_sellCar.text, 'html.parser')
    find_div = soup_2.find_all('div', attrs={'class': 'paging-inner'})
    get_div(find_div)


def get_div(div):
    number_page = []
    # find number of page link
    for ul in div:
        LI = ul.find_all('li')
        for tagA in LI:
            tag_a = tagA.find_all('a')
            for href in tag_a:
                if href.get('href'):
                    number_page.append(href.get('href'))
    number_page.insert(0, str(number_page[0].replace('page=2', 'page=1')))
    next_page(number_page)


def next_page(List):
    # next page
    link = str(List[len(List) - 1])
    for num in range(len(List) + 1, 501):
        new_page = 'page=' + str(num)
        page = link.replace('page=10', new_page)
        List.append(page)

    name_model(List)
    func_car(List)
    City(List)
    Price(List)


n_model = list()
m_model = list()


# get name and model of car
def name_model(List):
    for num in range(len(List)):
        page_link = requests.get(List[num])
        name_soup = BeautifulSoup(page_link.text, 'html.parser')
        name_car = name_soup.find_all('h2', attrs={'class': ['persianOrder', 'ad-title-span']})
        for n in name_car:
            ListOfName = re.sub(r'\s+', ' ', n.text).strip().split('،')
            if len(ListOfName) == 3:
                ListOfName.pop(2)
                n_model.append(str(ListOfName[0]))
                m_model.append(str(ListOfName[1].strip()))
            else:
                n_model.append(str(ListOfName[0]))
                m_model.append(str(ListOfName[1].strip()))


f_model = list()


def func_car(List):
    for num in range(len(List)):
        page_link = requests.get(List[num])
        name_soup = BeautifulSoup(page_link.text, 'html.parser')
        func = name_soup.find_all('div', attrs={'class': ['mid', 'price hidden-xs']})
        for funcs in func:
            # if funcs:
            number = re.search(r'\d+,\d*', funcs.p.text)
            if number:
                numberOffunc = str(number.group())
                f_model.append(numberOffunc)
            else:
                numberOffunc = str(funcs.p.text.strip())
                f_model.append(numberOffunc)


c_model = list()


def City(List):
    for num in range(len(List)):
        page_link = requests.get(List[num])
        name_soup = BeautifulSoup(page_link.text, 'html.parser')
        city = name_soup.find_all('div', attrs={'class': 'symbole visible-xs'})
        for cities in city:
            c = str(re.sub(r'\s+', ' ', cities.p.text).strip())
            c_model.append(c)



p_model = list()


def Price(List):
    for num in range(len(List)):
        page_link = requests.get(List[num])
        name_soup = BeautifulSoup(page_link.text, 'html.parser')
        price = name_soup.find_all('p', attrs={'class': 'cost'})
        for cost in price:
            final_cost = str(cost.span.text.strip())
            p_model.append(final_cost)
            print(price)


if __name__ == '__main__':
    bama_link()
    x = list(zip(p_model, c_model, f_model, m_model, n_model))
    for p, c, f, m, n in x:
        bama_backend.insert_name_model(n, m, f, c, p)
