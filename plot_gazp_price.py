# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Читаем данные из CSV
df = pd.read_csv('GAZP_history.csv')

# Удаляем строки с пустыми ценами (приостановка торгов)
df = df.dropna(subset=['CLOSE'])

# Преобразуем дату в datetime
df['TRADEDATE'] = pd.to_datetime(df['TRADEDATE'])

print(f'Всего записей после очистки: {len(df)}')
print(f'Период данных: с {df["TRADEDATE"].iloc[0].strftime("%Y-%m-%d")} по {df["TRADEDATE"].iloc[-1].strftime("%Y-%m-%d")}')

# Создаем график
plt.figure(figsize=(12, 6))
plt.plot(df['TRADEDATE'], df['CLOSE'], linewidth=1.5, color='blue', marker='o', markersize=1)
plt.title('Динамика цены акций Газпрома (GAZP)', fontsize=16)
plt.xlabel('Дата', fontsize=12)
plt.ylabel('Цена закрытия (руб.)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

# Добавляем информацию о минимуме и максимуме
min_price = df['CLOSE'].min()
max_price = df['CLOSE'].max()
min_date = df[df['CLOSE'] == min_price]['TRADEDATE'].iloc[0]
max_date = df[df['CLOSE'] == max_price]['TRADEDATE'].iloc[0]

plt.tight_layout()
plt.show()