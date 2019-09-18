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





#########################################################
# TODO-list:
# 1. 評分法 0.8 < (EPS*殖利率)/PER(本益比) < 1.2
# 2. 比較兩表相同的ID
    # coo = long_one
    # targets = short_one
    # (coo[:, None] == targets).any(1)
# 3. 
#########################################################
