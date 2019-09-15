import time
import requests
import datetime

import pandas as pd
from io import StringIO


def load_csv(year, month):
    df = pd.read_csv('data/monthly/%d_%d.csv' % (year, month))
    return df

def monthly(year, month):

    # 假如是西元，轉成民國
    if year > 1990:
        year -= 1911

    url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_' + \
        str(year)+'_'+str(month)+'_0.html'

    if year <= 98:
        url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_' + \
            str(year)+'_'+str(month)+'.html'

    # 偽瀏覽器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    # 下載該年月的網站，並用pandas轉換成 dataframe
    r = requests.get(url, headers=headers)
    r.encoding = 'big5'

    dfs = pd.read_html(StringIO(r.text), encoding='big-5')

    df = pd.concat([df for df in dfs if df.shape[1] <= 11 and df.shape[1] > 5])

    if 'levels' in dir(df.columns):
        df.columns = df.columns.get_level_values(1)
    else:
        df = df[list(range(0, 10))]
        column_index = df.index[(df[0] == '公司代號')][0]
        df.columns = df.iloc[column_index]

    df['當月營收'] = pd.to_numeric(df['當月營收'], 'coerce')
    df = df[~df['當月營收'].isnull()]
    df = df[df['公司代號'] != '合計']

    # 偽停頓
    time.sleep(5)

    return df

def cumulative(n_months, load_report, save_report):
    data = {}

    now = datetime.datetime.now()
    year = now.year
    month = now.month

    # 獲取近n個月的資料
    while len(data) < n_months:

        print('parsing', year, month)

        # 使用 crawlPrice 爬資料
        if load_report:
            try:
                data['%d-%d-01' % (year, month)] = load_csv(year, month)

            except:
                print('get 404, please check if the revenues are not revealed')

        else:
            try:
                data['%d-%d-01' % (year, month)] = monthly(year, month)

                if save_report:
                    data['%d-%d-01' % (year, month)].to_csv('data/monthly/%d_%d.csv' %
                                                            (year, month), encoding='utf-8', index=False)

            except:
                print('get 404, please check if the revenues are not revealed')

        # 減一個月
        month -= 1
        if month == 0:
            month = 12
            year -= 1

        time.sleep(10)

    return data
