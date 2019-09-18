import numpy as np
import pandas as pd

import datetime
import crawl_report


class StockScreenerMonth:
    def __init__(self, n_months=12, load_report=True, save_report=False):
        # 獲取近n個月的營收資料
        self.data_m = crawl_report.cast_n_months(n_months=12, load_report=True, save_report=False)
        # 數據處理─結合月營收資訊
        self.df_m = pd.DataFrame({k: df['當月營收'] for k, df in self.data_m.items()}).transpose().sort_index()

        # 初始化選股遮罩
        self.mask = np.ones(
            len(self.data_m[list(self.data_m)[0]]), dtype=np.int)
        self.mask_MoM_growth = np.ones(
            len(self.data_m[list(self.data_m)[0]]), dtype=np.int)
        self.mask_YoY_growth = np.ones(
            len(self.data_m[list(self.data_m)[0]]), dtype=np.int)
        self.mask_Total_YoY_growth = np.ones(
            len(self.data_m[list(self.data_m)[0]]), dtype=np.int)
        self.mask_Highest_revenue = np.ones(
            len(self.data_m[list(self.data_m)[0]]), dtype=np.int)
        self.mask_LongShortTerm_growth = np.ones(
            len(self.data_m[list(self.data_m)[0]]), dtype=np.int)
        self.mask_Trend_growth = np.ones(
            len(self.data_m[list(self.data_m)[0]]), dtype=np.int)

    def MoM_growth(self):
        # MoM > 0
        cond = self.data_m[list(self.data_m)[0]]['上月比較增減(%)'].astype(float) > 0
        self.mask_MoM_growth = np.asarray(cond)

    def YoY_growth(self):
        # Yoy > 0
        cond = self.data_m[list(self.data_m)[0]]['去年同月增減(%)'].astype(float) > 0
        self.mask_YoY_growth = np.asarray(cond)

    def Total_YoY_growth(self):
        #  Total_YoY > 0
        cond = self.data_m[list(self.data_m)[0]]['前期比較增減(%)'].astype(float) > 0
        self.mask_Total_YoY_growth = np.asarray(cond)

    def Highest_revenue(self):
        # 創新高法選股
        cond = self.df_m.iloc[-1] == self.df_m.iloc[-12:].max()
        self.mask_Highest_revenue = np.asarray(cond)

    def LongShortTerm_growth(self):
        # 平均線法選股
        cond = self.df_m.iloc[-3:].mean() > self.df_m.iloc[-12:].mean()
        self.mask_LongShortTerm_growth = np.asarray(cond)

    def Trend_growth(self):
        # 成長法選股
        cond = self.df_m.rolling(4, min_periods=2).mean()
        cond = (cond > cond.shift()).iloc[-5:].sum()
        self.mask_Trend_growth = np.asarray(cond)

    def Select_screener(self, 
                        _MoM_growth=True,
                        _YoY_growth=True,
                        _Total_YoY_growth=True,
                        _Highest_revenue=True,
                        _LongShortTerm_growth=True,
                        _Trend_growth=True):
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

        idx = np.where(self.mask > 0)

        # 參考營收增減評分並排序
        score = self.data_m[list(self.data_m)[0]].to_numpy()[idx, 5] + self.data_m[list(
            self.data_m)[0]].to_numpy()[idx, 6] + self.data_m[list(self.data_m)[0]].to_numpy()[idx, 9]
        argsort = np.flip(np.squeeze(np.argsort(score, axis=1)))

        # 只保留 [公司代號, 公司名稱]
        self.result = self.data_m[list(self.data_m)[0]].to_numpy()[idx, :2]
        self.result = np.squeeze(self.result, axis=0)

        # 按照評分分數遞減排序
        self.result = self.result[argsort, :]
        print(self.result)

    def Save_txt(self):
        now = datetime.datetime.now()
        filename = str(now.year)+'_'+str(now.month) + \
            '_'+str(now.day)+'_stock_list_month.txt'
        np.savetxt(filename, self.result, fmt='%s')
        print("The recommended stock list is saved !")



class StockScreenerSeason:
    def __init__(self, n_seasons=2, load_report=True, save_report=False):
        # 獲取近n個季的財報資料
        self.data_s = crawl_report.cast_n_seasons(n_seasons=2, load_report=True, save_report=False)
        # 數據處理─結合季毛利率資訊
        self.df_gpm = pd.DataFrame(
            {k: df['毛利率(%)(營業毛利)/(營業收入)'] for k, df in self.data_s.items()}).transpose().sort_index()
        # 數據處理─結合季營業利益率資訊
        self.df_opm = pd.DataFrame(
            {k: df['營業利益率(%)(營業利益)/(營業收入)'] for k, df in self.data_s.items()}).transpose().sort_index()
        # 數據處理─結合季稅後純益率資訊
        self.df_npm = pd.DataFrame(
            {k: df['稅後純益率(%)(稅後純益)/(營業收入)'] for k, df in self.data_s.items()}).transpose().sort_index()

        # 初始化選股遮罩
        self.mask = np.ones(
            len(self.data_s[list(self.data_s)[0]]), dtype=np.int)
        self.mask_GPM_growth = np.ones(
            len(self.data_s[list(self.data_s)[0]]), dtype=np.int)
        self.mask_OPM_growth = np.ones(
            len(self.data_s[list(self.data_s)[0]]), dtype=np.int)
        self.mask_NPM_growth = np.ones(
            len(self.data_s[list(self.data_s)[0]]), dtype=np.int)

    def GPM_growth(self):
        # 毛利率成長法選股
        cond1 = self.df_gpm.iloc[-2].astype(float) > 0
        cond2 = self.df_gpm.iloc[-1] > self.df_gpm.iloc[-2]
        self.mask_GPM_growth = np.asarray(cond1) & np.asarray(cond2)

    def OPM_growth(self):
        # 營業利益率成長法選股
        cond1 = self.df_opm.iloc[-2].astype(float) > 0
        cond2 = self.df_opm.iloc[-1] > self.df_opm.iloc[-2]
        self.mask_OPM_growth = np.asarray(cond1) & np.asarray(cond2)

    def NPM_growth(self):
        # 稅後純益率成長法選股
        cond1 = self.df_npm.iloc[-2].astype(float) > 0
        cond2 = self.df_npm.iloc[-1] > self.df_npm.iloc[-2]
        self.mask_NPM_growth = np.asarray(cond1) & np.asarray(cond2)

    def Select_screener(self, 
                        _GPM_growth=True,
                        _OPM_growth=True,
                        _NPM_growth=True):
        if _GPM_growth:
            self.GPM_growth()
        if _OPM_growth:
            self.OPM_growth()
        if _NPM_growth:
            self.NPM_growth()

    def Filter_stocks(self):
        self.mask = self.mask_GPM_growth & \
            self.mask_OPM_growth & self.mask_NPM_growth

        idx = np.where(self.mask > 0)
        
        # 參考營收增減評分並排序
        score  = self.data_s[list(self.data_s)[0]].to_numpy()[idx, 3] - self.data_s[list(self.data_s)[1]].to_numpy()[idx, 3]
        score += self.data_s[list(self.data_s)[0]].to_numpy()[idx, 4] - self.data_s[list(self.data_s)[1]].to_numpy()[idx, 4]
        score += self.data_s[list(self.data_s)[0]].to_numpy()[idx, 6] - self.data_s[list(self.data_s)[1]].to_numpy()[idx, 6]
        argsort = np.flip(np.squeeze(np.argsort(score, axis=1)))
        
        # 只保留 [公司代號, 公司名稱]
        self.result = self.data_s[list(self.data_s)[0]].to_numpy()[idx, :2]
        self.result = np.squeeze(self.result, axis=0)
        
        # 按照評分分數遞減排序
        self.result = self.result[argsort, :]
        print(self.result)

    def Save_txt(self):
        now = datetime.datetime.now()
        filename = str(now.year)+'_'+str(now.month) + \
            '_'+str(now.day)+'_stock_list_season.txt'
        np.savetxt(filename, self.result, fmt='%s')
        print("The recommended stock list is saved !")
