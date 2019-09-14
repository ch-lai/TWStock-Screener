import datetime
import argparse
import numpy as np
import pandas as pd
import crawl_report


# 獲取近n個月的營收資料
data = crawl_report.cast_n_months(n_months = 12, load_report = True, save_report = False)

# 數據處理─結合月營收資訊
for k in data.keys():
    data[k].index = data[k]['公司代號']+' '+data[k]['公司名稱']
    
df = pd.DataFrame({k:df['當月營收'] for k, df in data.items()}).transpose()
df.index = pd.to_datetime(df.index)
df = df.sort_index()

# 平均線法選股
method1 = df.iloc[-3:].mean() > df.iloc[-12:].mean()
method1[method1 == True].index

# 創新高法選股
method2 = df.iloc[-1] == df.iloc[-12:].max()
method2[method2 == True].index

# 成長法選股
method3 = df.rolling(4, min_periods=2).mean()
method3 = (method3 > method3.shift()).iloc[-5:].sum()
method3[method3 == 5].index


# save list to txt
stock_list = np.asarray(method3[method3 == 5].index)

now = datetime.datetime.now()
filename = str(now.year)+'_'+str(now.month)+'_'+str(now.day)+'_stock_list.txt'
np.savetxt(filename, stock_list, fmt='%s')
print("The recommended stock list is saved !")