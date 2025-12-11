import requests
import json
import pandas as pd

ticker = "GAZP"
date = "2025-12-05"

url = f"https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities/{ticker}.json"
params = {'from': date, 'till': date}

response = requests.get(url, params=params)
data = response.json()

columns = data['history']['columns']
rows = data['history']['data']

if rows:
    # Создаем словарь со всеми полями
    full_data = dict(zip(columns, rows[0]))
    
    print(f"ВСЕ доступные данные по {ticker} за {date}:\n")
    for key, value in full_data.items():
        print(f"{key:20} = {value}")
    
    # Сохраняем в JSON
    with open('gazprom_full_data.json', 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)
    
    # Сохраняем в CSV
    df = pd.DataFrame([full_data])
    df.to_csv('gazprom_full_data.csv', index=False)
    
    print(f"\n\nВсего полей: {len(full_data)}")
    print("Данные сохранены в gazprom_full_data.json и gazprom_full_data.csv")
else:
    print(f"Нет данных за {date}")


# Идентификация:
# BOARDID = TQBR - режим торгов (Т+ Основной режим, акции первого уровня)
# TRADEDATE = 2025-12-05 - дата торгов
# SHORTNAME = ГАЗПРОМ ао - краткое название компании
# SECID = GAZP - тикер (код акции)

# Цены (в рублях):
# OPEN = 125.35 - цена открытия торгов
# HIGH = 128.8 - максимальная цена за день
# LOW = 125.22 - минимальная цена за день
# CLOSE = 128.67 - цена последней сделки
# LEGALCLOSEPRICE = 128.54 - официальная цена закрытия (для расчетов)
# WAPRICE = 127.67 - средневзвешенная цена (по объему всех сделок)

# Рыночные цены:
# MARKETPRICE2 = 127.71 - рыночная цена (для маржинальных позиций)
# MARKETPRICE3 = 127.71 - рыночная цена (альтернативный расчет)
# ADMITTEDQUOTE = пусто - допущенная котировка

# Объемы торгов:
# VOLUME = 61,368,000 - количество акций (61.4 млн штук)
# VALUE = 7,836,333,211.7 - оборот в рублях (7.8 млрд руб)
# NUMTRADES = 84,641 - количество сделок за день
# Объемы по типам цен:
# MP2VALTRD = 6,802,050,354.6 - оборот по рыночной цене 2
# MARKETPRICE3TRADESVALUE = 6,802,050,354.6 - оборот по рыночной цене 3
# ADMITTEDVALUE = пусто - оборот по допущенной котировке
# WAVAL = 0 - взвешенный средний объем

# Дополнительно:
# TRADINGSESSION = 3 - номер торговой сессии
# CURRENCYID = SUR - валюта (рубль)
# TRENDCLSPR = 2.67 - изменение цены закрытия (+2.67 руб к предыдущему дню)
# TRADE_SESSION_DATE = 2025-12-05 - дата торговой сессии
# Итог по Газпрому 05.12.2025:
# Рост с 125.35 до 128.67 руб (+2.65%)
# Оборот 7.8 млрд руб
# 84,641 сделка