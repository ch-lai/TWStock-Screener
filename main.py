#########################################################
# TODO-list:
# 1. 0.8 < (EPS*殖利率)/PER(本益比) < 1.2 (評分法或用來判斷買入點)
# 2. 爬 "綜合損益彙總表"，並加入feature (Crawl Statement of Comprehensive Income)
# 3. 90% < 營業利益（損失）/(營業利益（損失）+ 營業外收入及支出) < 110%
# 4. 4季財報成長法、4季累積ROE > 8%、EPS 持續正成長
# 5. 選出後，畫出近一個月K線圖，並結合技術指標提供買點
# 6. 比較兩表相同的ID
    # coo = long_one
    # targets = short_one
    # (coo[:, None] == targets).any(1)
#########################################################

from stock_screener import StockScreenerMonth
from stock_screener import StockScreenerSeason


# Init StockScreener type
ss = StockScreenerMonth()
ss = StockScreenerSeason()

# Select multiple screener methods
ss.Select_screener()

# Filter stocks
ss.Filter_stocks()

# Save in txt
ss.Save_txt()
