import httpx
from bs4 import BeautifulSoup
import pandas as pd
import asyncio
import time
import csv
import scraper as sh
import ast

def requests(url, headers):
    r = httpx.get(url, headers=headers)
    soup = BeautifulSoup(r.content,'lxml')
    li_of_first = []
    for links in soup.find_all('div', class_='category-image'):
        link_1 = links.find('a').get('href')
        li_of_first.append(link_1)
    return li_of_first
def requests_2(test_url, headers):
    global link_2
    timeout = httpx.Timeout(10.0 , read=None)
    r = httpx.get(test_url, headers=headers ,timeout=timeout)
    soup = BeautifulSoup(r.content,'lxml')
    li_2 = []
    for links in soup.find_all('div', class_='grid-buy-button'):
        try :
                link_2 = links.find('a').get('href')
                li_2.append(link_2)
        except AttributeError :
            link_2 = test_url
            li_2.append(link_2)
    return li_2
#test_url_2 = 'https://www.air-masters.eu/de/luftvorhaenge-airmasters/305-677-luftvorhang-airmasters-plus-02-51mm.html#/27-material-aluminium_beschichtet'
def parse(url_list , headers):
    timeout = httpx.Timeout(10.0 , read=None)
    r = httpx.get(url_list, headers=headers, timeout=timeout)
    soup = BeautifulSoup(r.content,'lxml')
    product_list = []
    try:
        for pro in soup.find_all('div', id = "mainProduct"):
            product = {
                'id' : pro.find('h1', class_='page-heading').text,
                'description' : pro.find('div',itemprop="description" ).find('p').text,
                'iamges' : pro.find('img').get('src'),
                'url': url_list,
            }
    except AttributeError:
        product = {
                'id' : 'none',
                'description' : 'none',
                'iamges' : 'none',
                'url': url_list,
            }
    #product_list.append(product)
    return product

def save_to_csv(last):
    df = pd.DataFrame(last)
    df.to_csv('air_data.csv', index=False)


def main():
    second_list = []
    main_list = []
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
    start_url = 'https://www.air-masters.eu/de/'
    first = requests(start_url,headers)
    print(first ,len(first))
    x = 1
    for list_of in first:
        second = requests_2(list_of, headers)
        second_list.append(second)
        # print(second_list)
        # len(second_list)
        for third in second:
            last = parse(third , headers)
            print(x)
            x += 1
            main_list.append(last)
            print(main_list)
            save_to_csv(main_list)
    save_to_csv(main_list)

    print('saved to csv ...')

if __name__ == "__main__":

    main()

    
    