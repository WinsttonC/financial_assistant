import pytz
import requests
from datetime import datetime


import pytz
import requests

from time import sleep
from pytz import timezone

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'accept': '*/*',
    'content-type': 'application/x-www-form-urlencoded',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}

link = 'https://www.tinkoff.ru/api/invest-gw/social/v1/post/instrument/{}?limit=50&appName=invest&platform=web&cursor={}'


def get_data_from_api(url: str, ticker: str, cursor_number: str, min_time: str = None, max_time: str = None) -> list:
    link = url.format(ticker, cursor_number)
    session = requests.Session()
    data = session.get(link, headers=headers, stream=True)
    raw_data = data.json().get('payload').get('items')
    filtered_results = []

    # Helper function to parse datetime with timezone
    try:
        for i in raw_data:
            d = {
                'likesCount': i['likesCount'],
                'commentsCount': i['commentsCount'],
                'inserted': i['inserted'],
                'nickname': i['nickname'],
                'ticker_mentioned': [x['ticker'] for x in i['instruments']],
                'ticker_company_name': [x['briefName'] for x in i['instruments']],
                'text': i['content']['text']
            }
            filtered_results.append(d)
    except:
        pass

    return filtered_results
