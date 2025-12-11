# -*- coding: utf-8 -*-
import requests
import pandas as pd
from datetime import datetime, timedelta

# Параметры
ticker = 'GAZP'
start_date = '2006-01-01'
end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')  # Вчерашний день

with requests.Session() as session:
    # Получение исторических данных по ГАЗП
    # Попробуем другие режимы торгов
    boards = ['TQBR', 'EQBR', 'SMAL']  # Основные, Основные-2, Малые
    all_data = []
    columns = None
    
    for board in boards:
        print(f'Проверяем режим {board}...')
        url = f'https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/{board}/securities/{ticker}.json'
        params = {
            'from': start_date,
            'till': end_date,
            'start': 0
        }
        
        board_data = []
        
        # Получаем данные порциями
        while True:
            response = session.get(url, params=params)
            data = response.json()
            
            if not data['history']['data']:
                break
                
            board_data.extend(data['history']['data'])
            params['start'] += 100
        
        if board_data:
            print(f'Найдено {len(board_data)} записей на режиме {board}')
            if columns is None:
                columns = data['history']['columns']
            all_data.extend(board_data)
        else:
            print(f'На режиме {board} данных нет')
    
    if not all_data:
        print('Никаких данных не найдено')
        exit()
    
    # Создаем DataFrame
    df = pd.DataFrame(all_data, columns=columns)
    
    # Удаляем дубликаты по дате
    df = df.drop_duplicates(subset=['TRADEDATE']).sort_values('TRADEDATE')
    
    # Сохраняем в CSV
    df[['TRADEDATE', 'CLOSE']].to_csv(f'{ticker}_history.csv', index=False, encoding='utf-8')
    
    print(f'Загружено {len(df)} записей с {start_date} по {end_date}')
    print('Доступные колонки:', df.columns.tolist())
    print('\nПервые 5 записей:')
    print(df[['TRADEDATE', 'CLOSE', 'VOLUME', 'VALUE']].head(5))