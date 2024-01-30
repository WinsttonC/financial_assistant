import os
from telethon.sync import TelegramClient
from asyncio import run
import pandas as pd


api_id = os.getenv("API_TELEGRAM_ID")
api_hash = 'HASH'
api_hash = str(api_hash)
phone = 'NUMBER'
name = "NAME"


chat = 'https://t.me/cbrstocks'
f_name = chat.replace("https://t.me/", "")
path = f'PATH'

com = []
def get_data(chat):
  df = pd.DataFrame(columns = ['date', 'views', 'count_reaction','top_reaction', 'forward', 'media','scheduled', 'edit_date',  'edit_hide', 'text', 'comments'])

  async def messages_func(name, api_id, api_hash):
    i = 0
    async with TelegramClient(name, api_id, api_hash) as client:
      print("Extracting messages")
      messages = client.iter_messages(chat)
      
      async for message in messages:
        id_1 = message.id
        text = message.message
        views = message.views
        date = message.date
        from_scheduled = message.from_scheduled
        edit_date = message.edit_date
        edit_hide = message.edit_hide
        reac = message.reactions
        med = message.media
        com = []

        forward = message.forwards
        df.at[id_1, 'text'] = text
        df.at[id_1, 'forward'] = forward
        df.at[id_1, 'views'] = views
        df.at[id_1, 'date'] = date
        df.at[id_1, 'media'] = med
        df.at[id_1, 'top_reaction'] = reac
        df.at[id_1, 'scheduled'] = from_scheduled
        df.at[id_1, 'edit_date'] = edit_date
        df.at[id_1, 'edit_hide'] = edit_hide  

        if i > 2000:
          break     

  run(messages_func(name, api_id, api_hash))

  df = df.reset_index(names='index')
  df.to_csv(path, index=False)

chats = [
  'https://t.me/cbrstocks',
  'https://t.me/centralbank_russia',
  'https://t.me/alfawealth',
  'https://t.me/dohod',
  'https://t.me/MoscowExchangeOfficial',
  'https://t.me/SberInvestments'

]
for chat in chats:
  print('Сейчас обрабатывается канал: ', chat)
  get_data(chat)
