from datetime import datetime
from datetime import timedelta
from time import time
from pathlib import Path
import time_recorder

def get_difference():
    total = 0
    tday_total = time_recorder.get_today_record()
    yday = datetime.now() - timedelta(days=1)

    path = f'./data/{yday.year}/'
    with open(f'{path}time_record.csv', 'r', encoding='utf-8') as f:
        for row in f:
            columns = row.split(',')
            date = columns[0]
            t = int(columns[2])
            datetime_date = datetime.strptime(date, '%Y/%m/%d')
            if datetime_date.day == yday.day:
                total += t
    
    total = tday_total - total
    if total >= 0:
        result = time_recorder.dmod(total)
        return f'+ {result}'
    else:
        result = time_recorder.dmod(abs(total))
        return f'- {result}'

print(get_difference())