import time
import requests
import datetime

import numpy as np
import pandas as pd
from io import StringIO


def load_csv(year, month, type):
    if type == 'monthly':
        df = pd.read_csv('data/monthly/%d_%d.csv' % (year, month))
    elif type == 'seasonal':
        df = pd.read_csv('data/seasonal/%d_%d.csv' % (year, month))
    else:
        print('get 404, wrong type')

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

    return df

def seasonal(year, season, type='營益分析彙總表'):

    # 假如是西元，轉成民國
    if year > 1990:
        year -= 1911

    if type == '營益分析彙總表':
        url = 'https://mops.twse.com.tw/mops/web/ajax_t163sb06'

        r = requests.post(url, {
            'encodeURIComponent': 1,
            'step': 1,
            'firstin': 1,
            'off': 1,
            'TYPEK': 'sii',
            'year': str(year),
            'season': str(season),
        })

        r.encoding = 'utf8'
        dfs = pd.read_html(r.text)

        for i, df in enumerate(dfs):
            df.columns = df.iloc[0]
            dfs[i] = df.iloc[1:]

        df = pd.concat(dfs, sort=False).applymap(
            lambda x: x if x != '--' else np.nan)
        df = df[df['公司代號'] != '公司代號']
        df = df[~df['公司代號'].isnull()]

    elif type == '綜合損益彙總表':
        url = 'https://mops.twse.com.tw/mops/web/ajax_t163sb04'

        r = requests.post(url, {
            'encodeURIComponent': 1,
            'step': 1,
            'firstin': 1,
            'off': 1,
            'TYPEK': 'sii',
            'year': str(year),
            'season': str(season),
        })

        r.encoding = 'utf8'
        dfs = pd.read_html(r.text)

        df = pd.concat([df for df in dfs if df.shape[1] > 10], sort=False)        
        df.columns = df.columns.get_level_values(0)

        df['營業利益（損失）'] = pd.to_numeric(df['營業利益（損失）'], 'coerce')
        df['營業外收入及支出'] = pd.to_numeric(df['營業外收入及支出'], 'coerce')
        df['基本每股盈餘（元）'] = pd.to_numeric(df['基本每股盈餘（元）'], 'coerce')
        df = df[~df['營業利益（損失）'].isnull()]
        df = df[~df['營業外收入及支出'].isnull()]
        df = df[~df['基本每股盈餘（元）'].isnull()]

    # elif type == '資產負債彙總表':
    #     url = 'https://mops.twse.com.tw/mops/web/ajax_t163sb05'
    else:
        print('type does not match')

    return df


def cast_n_months(n_months, load_report, save_report):
    data = {}

    now = datetime.datetime.now()
    year = now.year
    month = now.month

    # 獲取近n個月的資料
    while len(data) < n_months:
        print('parsing', year, month)

        if load_report:
            try:
                data['%d-%d-01' %
                     (year, month)] = load_csv(year, month, type='monthly')

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


def cast_n_seasons(n_seasons, load_report, save_report):
    data = {}

    now = datetime.datetime.now()
    year = now.year
    month = now.month

    if month <= 3:
        season = 1
    elif month <= 6:
        season = 2
    elif month <= 9:
        season = 3
    elif month <= 12:
        season = 4
    else:
        print('get 404, please check if the season is conrrect')

    # 獲取近n個季的資料
    while len(data) < n_seasons:
        print('parsing', year, season)

        if load_report:
            try:
                data['%d-%d-01' %
                     (year, season)] = load_csv(year, season, type='seasonal')

            except:
                print('get 404, please check if the financial reports are not revealed')

        else:
            try:
                data['%d-%d-01' % (year, season)] = seasonal(year, season, type='營益分析彙總表')

                if save_report:
                    data['%d-%d-01' % (year, season)].to_csv('data/seasonal/營益分析彙總表/%d_%d.csv' %
                                                             (year, season), encoding='utf-8', index=False)

            except:
                print('get 404, please check if the financial reports are not revealed')

        # 減一季
        season -= 1
        if season == 0:
            season = 4
            year -= 1

        time.sleep(10)

    return data
