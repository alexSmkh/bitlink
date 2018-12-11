import requests
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
import sys


load_dotenv()


def make_bitlink(access_token, url):
    header = {
        'Authorization': 'Bearer ' + access_token
    }
    data = {
        'long_url': url
    }
    url_for_request = 'https://api-ssl.bitly.com/v4/bitlinks'
    response_with_bitlink_data = requests.post(url=url_for_request, headers=header, json=data)
    if response_with_bitlink_data.ok:
        bitlink = response_with_bitlink_data.json()['link']
        return bitlink


def load_clicks_for_bitlink(access_token, url):
    bitlink = get_formatted_link(url)
    url_for_request = \
        'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'.format(
            bitlink=bitlink
        )
    header = {
        'Authorization': 'Bearer ' + access_token
    }
    data = {
        'bitlink': bitlink,
    }
    params = {
        'unit': 'month'
    }
    response_with_clicks = requests.get(
        url=url_for_request,
        headers=header,
        json=data,
        params=params
    )

    if response_with_clicks.ok:
        click_info = response_with_clicks.json()
        return click_info['total_clicks']
    else:
        bitlink = make_bitlink(access_token, url)
        return bitlink


def get_formatted_link(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme:
        scheme = "%s://" % parsed_url.scheme
        return parsed_url.geturl().replace(scheme, '', 1)
    else:
        return url


if __name__ == '__main__':
    access_token = os.getenv('TOKEN')
    url_for_request = sys.argv[1]
    info_for_printing = load_clicks_for_bitlink(access_token, url_for_request)
    if info_for_printing is None:
        print('Ошибка')
    else:
        print(info_for_printing)