from stock_screener import StockScreener


# Init StockScreener
ss = StockScreener(n_months=12, load_report=True, save_report=False)

# Select multiple screener methods
ss.Select_screener(_MoM_growth=True,
                   _YoY_growth=True,
                   _Total_YoY_growth=True,
                   _Highest_revenue=True,
                   _LongShortTerm_growth=True,
                   _Trend_growth=True)

# Filter stocks
ss.Filter_stocks()

# Save in txt
ss.Save_txt()
