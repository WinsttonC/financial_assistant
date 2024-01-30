import requests
import requests
from datetime import datetime
import pandas as pd
import os

TOKEN_USER = os.getenv("TOKEN_USER_VK")
VERSION = '5.84'

domains = [
      'https://vk.com/bcs_world_of_investments',
      'https://vk.com/ixbt_official',
      'https://vk.com/investingcom',
      'https://vk.com/rbc_investments',
      'https://vk.com/brokervtb',
      'https://vk.com/incrussiamedia',
      'https://vk.com/investments_tinkoff',
      'https://vk.com/kommersant.economics'
]

def get_data(DOMAIN):
    
    DOMAIN = DOMAIN.replace("https://vk.com/", "")
    name = DOMAIN
    path = f'../data/raw/{name}.csv'
    
    data = []
    offset = 0
    for i in range(40):
            try:
                    response = requests.get('https://api.vk.com/method/wall.get',
                    params={'access_token': TOKEN_USER,
                    'v': VERSION,
                    'domain': DOMAIN,
                    'offset': offset,
                    'count': 100,
                    'filter': str('owner')})

                    data1 = response.json()['response']['items']
                    for elem in data1:
                            data.append(elem)
                    offset += 100
            except Exception as e:
                    print(e)
                    break

    df = pd.DataFrame(columns = ['date', 'owner_id', 'likes.count', 'comments.count', 'reposts.count', 'views.count', 'text'])
    id = ''
    for elem in data:
        id_1 = elem['id']
        df.loc[id_1, 'owner_id'] = elem['owner_id']
        df.loc[id_1, 'likes.count'] = elem['likes']['count']
        df.loc[id_1, 'comments.count']= elem['comments']['count']
        df.loc[id_1, 'reposts.count'] = elem['reposts']['count']
        try:
            df.loc[id_1, 'views.count'] = elem['views']['count']
        except:
            continue
        df.loc[id_1, 'text'] = elem['text'] = elem['text']
        df.loc[id_1, 'date'] = datetime.fromtimestamp(elem['date'])

    df = df.reset_index()
    df.to_csv(path, index=False)

for domain in domains:
    print(f'Сейчас обрабатывается канал: {domain}')
    get_data(domain)
    