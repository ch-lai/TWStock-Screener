import numpy as np
import pandas as pd

import datetime
import crawl_report


class StockScreener:
    def __init__(self, n_months=12, load_report=True, save_report=False):
        # 獲取近n個月的營收資料
        self.data = crawl_report.cumulative(
            n_months=12, load_report=True, save_report=False)

        # 數據處理─結合月營收資訊
        self.df = pd.DataFrame(
            {k: df['當月營收'] for k, df in self.data.items()}).transpose().sort_index()

        # 初始化選股遮罩
        self.mask = np.ones(
            len(self.data[list(self.data)[0]]), dtype=np.int)
        self.mask_MoM_growth = np.ones(
            len(self.data[list(self.data)[0]]), dtype=np.int)
        self.mask_YoY_growth = np.ones(
            len(self.data[list(self.data)[0]]), dtype=np.int)
        self.mask_Total_YoY_growth = np.ones(
            len(self.data[list(self.data)[0]]), dtype=np.int)
        self.mask_Highest_revenue = np.ones(
            len(self.data[list(self.data)[0]]), dtype=np.int)
        self.mask_LongShortTerm_growth = np.ones(
            len(self.data[list(self.data)[0]]), dtype=np.int)
        self.mask_Trend_growth = np.ones(
            len(self.data[list(self.data)[0]]), dtype=np.int)

    def MoM_growth(self):
        # MoM > 0
        cond = self.data[list(self.data)[0]]['上月比較增減(%)'].astype(float) > 0
        self.mask_MoM_growth = np.asarray(cond)

    def YoY_growth(self):
        # Yoy > 0
        cond = self.data[list(self.data)[0]]['去年同月增減(%)'].astype(float) > 0
        self.mask_YoY_growth = np.asarray(cond)

    def Total_YoY_growth(self):
        #  Total_YoY > 0
        cond = self.data[list(self.data)[0]]['前期比較增減(%)'].astype(float) > 0
        self.mask_Total_YoY_growth = np.asarray(cond)

    def Highest_revenue(self):
        # 創新高法選股
        cond = self.df.iloc[-1] == self.df.iloc[-12:].max()
        self.mask_Highest_revenue = np.asarray(cond)

    def LongShortTerm_growth(self):
        # 平均線法選股
        cond = self.df.iloc[-3:].mean() > self.df.iloc[-12:].mean()
        self.mask_LongShortTerm_growth = np.asarray(cond)

    def Trend_growth(self):
        # 成長法選股
        cond = self.df.rolling(4, min_periods=2).mean()
        cond = (cond > cond.shift()).iloc[-5:].sum()
        self.mask_Trend_growth = np.asarray(cond)

    def Select_screener(self, _MoM_growth=False,
                        _YoY_growth=False,
                        _Total_YoY_growth=False,
                        _Highest_revenue=False,
                        _LongShortTerm_growth=False,
                        _Trend_growth=False):
        if _MoM_growth:
            self.MoM_growth()
        if _YoY_growth:
            self.YoY_growth()
        if _Total_YoY_growth:
            self.Total_YoY_growth()
        if _Highest_revenue:
            self.Highest_revenue()
        if _LongShortTerm_growth:
            self.LongShortTerm_growth()
        if _Trend_growth:
            self.Trend_growth()

    def Filter_stocks(self):
        self.mask = self.mask_MoM_growth & self.mask_YoY_growth & \
            self.mask_Total_YoY_growth & self.mask_Highest_revenue & \
            self.mask_LongShortTerm_growth & self.mask_Trend_growth

    def Save_txt(self):
        now = datetime.datetime.now()
        filename = str(now.year)+'_'+str(now.month) + \
            '_'+str(now.day)+'_stock_list.txt'
        np.savetxt(filename, self.mask, fmt='%s')
        print("The recommended stock list is saved !")
