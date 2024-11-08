# import requests
# from bs4 import BeautifulSoup

# headers = {
#     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'
# }

# proxies = {
#     'https': 'http://89.218.175.84:8080'
#     # 'https': f'http://{login}:{password}@proxy_ip:proxy_port'
# }


# def get_location(url):
#     response = requests.get(url=url, headers=headers, proxies=proxies, timeout=7)
#     soup = BeautifulSoup(response.text, 'lxml')

#     ip = soup.find('div', class_='ip').text.strip()
#     location = soup.find('div', class_='value-country').text.strip()

#     print(f'IP: {ip}\nLocation: {location}')


# def main():
#     get_location(url='https://2ip.ru')


# if __name__ == '__main__':
#     main()


import requests
from bs4 import BeautifulSoup
import multiprocessing


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'
}


def handler(proxy):
    proxies = {
        # 'http': f'http://{proxy}',
        'https': f'http://inulgvqm:drzeljplcnbh@{proxy}'
    }

    url = 'https://2ip.ru'
    try:
        response = requests.get(url=url, headers=headers, proxies=proxies, timeout=7)
        soup = BeautifulSoup(response.text, 'lxml')

        ip = soup.find('div', class_='ip').text.strip()
        location = soup.find('div', class_='value-country').text.strip()

        print(f'IP: {proxy}\nLocation: {location}')
    except:
        ...


with open('Webshare 10 proxies.txt') as file:
    proxy_base = ''.join(file.readlines()).strip().split('\n')


with multiprocessing.Pool(4) as process:
    process.map(handler, proxy_base)

# handler('64.64.118.149:6732')
