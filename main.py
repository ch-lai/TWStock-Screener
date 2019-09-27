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
