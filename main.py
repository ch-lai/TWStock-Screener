#########################################################
# TODO-list:
# 1. 評分法 0.8 < (EPS*殖利率)/PER(本益比) < 1.2
# 2. 比較兩表相同的ID
    # coo = long_one
    # targets = short_one
    # (coo[:, None] == targets).any(1)
# 3. 4季財報成長法
# 4. 90% < 營業利益（損失）/(營業利益（損失）+ 營業外收入及支出) < 110%
# 5. ROE > 8%
# 6. 爬 "綜合損益彙總表"，並加入feature
# 7. 選出後，畫出近一個月K線圖，並結合技術指標提供買點
#########################################################

from stock_screener import StockScreenerMonth
from stock_screener import StockScreenerSeason


# Init StockScreener type
# ss = StockScreenerMonth()
ss = StockScreenerSeason()

# Select multiple screener methods
ss.Select_screener()

# Filter stocks
ss.Filter_stocks()

# Save in txt
ss.Save_txt()
