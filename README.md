# Taiwan Stock Market Screener (Search and Filter Stocks)
This repository is inspired by [finlab Blog](https://www.finlab.tw/).

According to statistics, 80% of the people in the world don't like their job. If you are one of them, you should know how to manage your finances. For whom are beginners, here are some guides you should read before you investigate your money in the stock market.

## Disclaimers
This is only my personal research. I DO NOT recommend you to use it as your trading strategy, and I CAN NOT guarantee you any feasibility. You should make your own judgement and take it only as a reference. GOOD LUCK!


## ToDo-List
- [x] Crawl monthly revenue from TWSE
- [x] Support three stock screener methods based on monthly revenue
- [ ] Crawl seansonal financial reports from TWSE
- [ ] Support more stock screener methods based on financial reports
- [ ] To be more robust with the integration of the methods above
- [ ] Backtest every stock screener methods
- [ ] ...


## Getting Started
Implemented and tested on Ubuntu 18.04 with Python 3.6.

1. Clone this repo
```bash
git clone https://github.com/ch-lai/TWStock-Screener.git
```

2. Install Python dependencies
```bash
cd TWStock-Screener
pip3 install -r requirements.txt
```

3. Run the scripts
```bash
python main.py
```

## Report Issue
- Issues: https://github.com/ch-lai/TWStock-Screener/issues

## LICENSE
Copyright (c) 2019 [Chao-Hsiang Lai](https://github.com/ch-lai)