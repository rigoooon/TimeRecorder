from datetime import datetime
from datetime import timedelta
from pathlib import Path
import os

#今日の合計時間を出力
def get_today_record():
    total = 0 
    present_time = datetime.now()
    path = f'./data/{present_time.year}/'

    with open(f'{path}time_record.csv', 'r', encoding='utf-8') as f:
        for row in f:
            columns = row.split(',')
            date = columns[0]
            t = int(columns[2])
            datetime_date = datetime.strptime(date, '%Y/%m/%d')
            if datetime_date.day == present_time.day:
                total += t

    return total

#前日との差
def get_difference():
    total = 0
    tday_total = get_today_record()
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
        result = dmod(total)
        return f'+ {result}'
    else:
        result = dmod(abs(total))
        return f'- {result}'

#今日を含めた一週間の合計時間
def get_this_week_record():
    total = 0
    present_time = datetime.now()
    for i in range(7):
        pr_time = present_time - timedelta(days=i)
        path = f'./data/{pr_time.year}/'
        with open(f'{path}time_record.csv', 'r', encoding='utf-8') as f:
            for row in f:
                columns = row.split(',')
                date = columns[0]
                t = int(columns[2])
                datetime_date = datetime.strptime(date, '%Y/%m/%d')
                if datetime_date.day == pr_time.day:
                    total += t
    return total

#一週間の日ごとの時間を一括表示
def get_weekly_record():
    total_dict = {}
    p_time = datetime.now()
    for i in range(7):
        total = 0
        pr_time = p_time - timedelta(days=i)
        with open('time_record.csv', 'r', encoding='utf-8') as f:
            for row in f:
                columns = row.split(',')
                date = columns[0]
                t = int(columns[2])
                datetime_date = datetime.strptime(date, '%Y/%m/%d')
                if datetime_date.day == pr_time.day:
                    total += t
        result = dmod(total)
        if f'{pr_time:%Y/%m/%d}' not in total_dict.keys():
            total_dict[f'{pr_time:%Y/%m/%d}'] = result
    return total_dict

def get_this_year_record():
    total = 0
    present_time = datetime.now()

    path = f'./data/{present_time.year}/'
    with open(f'{path}time_record.csv', 'r', encoding='utf-8') as f:
        for row in f:
            columns = row.split(',')
            date = columns[0]
            seconds = int(columns[2])
            datetime_date = datetime.strptime(date, '%Y/%m/%d')
            if datetime_date.year == present_time.year:
                total += seconds
    return total

#今月の合計時間を出力
def get_this_month_record():
    total = 0
    present_time = datetime.now()

    path = f'./data/{present_time.year}/'
    with open(f'{path}time_record.csv', 'r', encoding='utf-8') as f:
        for row in f:
            columns = row.split(',')
            date = columns[0]
            seconds = int(columns[2])
            datetime_date = datetime.strptime(date, '%Y/%m/%d')
            if datetime_date.month == present_time.month:
                total += seconds

    return total


#記録した全ての合計
def get_all_records():
    total = 0
    for year in os.listdir('./data/'):
        if year == '.DS_Store':
            continue
        else:
            with open(f'./data/{year}/time_record.csv', 'r', encoding='utf-8') as f:
                for row in f:
                    columns = row.split(',')
                    seconds = int(columns[2])
                    total += seconds
    return total

#秒単位で記録された時間を分、時間に換算する
def dmod(total):
    hour = 0
    minute = 0
    second = 0
    
    if total >= 60:
        minute, second = divmod(total, 60)
        if minute >= 60:
            hour, minute = divmod(minute, 60)
    else:
        minute = 0
        second = total

    return f'{int(hour)}h{int(minute)}m{int(second)}s'





