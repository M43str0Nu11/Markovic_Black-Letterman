# -*- coding: utf-8 -*-
import requests
import pandas as pd

with requests.Session() as session:
    
    # Получение спецификации инструмента / Описание инстрмуента
    ticker = 'GAZP'
    url = f'https://iss.moex.com/iss/securities/{ticker}.json' 
    response = session.get(url)
    data = response.json()
    df = pd.DataFrame(data['description']['data'], columns=data['description']['columns'])
    
    # Список бумаг торгуемых на московвской бирже\
    url2 = 'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json'
    response2 = session.get(url2)
    data2 = response2.json()
    df2 = pd.DataFrame(data2['securities']['data'], columns=data2['securities']['columns'])

df.to_csv(f'{ticker}_full_description', index=False, encoding='utf-8')
df2[['SECID', 'SHORTNAME', 'SECNAME']].to_csv('tickers_moex', index=False, encoding='utf-8')

#print(df2.columns.tolist()) получение листа столбцов
print(f'\nПолное описание {ticker}:')
print(df)

#.venv\Scripts\activate
#deactivate