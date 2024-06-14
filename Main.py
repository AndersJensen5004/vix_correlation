########################
# Anders Jensen - 2024
# Main.py
########################

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


class Ticker:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def get_prices(self, start_date: str, end_date: str) -> pd.DataFrame:
        try:
            data = yf.download(self.symbol, start=start_date, end=end_date)
            return data['Close']
        except Exception as e:
            print(e)

    def get_returns(self, period: int, start_date: str, end_date: str) -> list[tuple]:
        returns = []
        try:
            prices = self.get_prices(start_date, end_date)
            for i in range(len(prices) - period):
                start_price = prices.iloc[i]
                end_price = prices.iloc[i + period]
                period_change = ((end_price - start_price) / start_price) * 100
                period_start_date = prices.index[i]
                # period_end_date = prices.index[i + period]
                returns.append((period_start_date, period_change))
            return returns
        except Exception as e:
            print(e)

    @staticmethod
    def add_vix(returns: list[tuple]) -> list[tuple]:
        vix = Ticker('^VIX')
        vix_levels = vix.get_prices(returns[0][0], returns[-1][0])
        vix_levels_dict = vix_levels.to_dict()

        for i in range(len(returns)):
            start_date = returns[i][0]
            if start_date in vix_levels_dict:
                vix_level = vix_levels_dict[start_date]
                returns[i] = (start_date, returns[i][1], vix_level)
            else:
                print(f"VIX not found for {start_date}")
                returns.remove(returns[i])

        return returns


if __name__ == "__main__":
    # Trading days in periods
    year_length = 252
    three_month_length = 63
    month_length = 21
    week_length = 5

    SPX = Ticker('^GSPC')
    SPX_prices = SPX.get_prices('1990-01-01', '2024-05-01')
    SPX_returns = SPX.get_returns(month_length, '1990-01-01', '2024-05-01')

    SPX_VIX = Ticker.add_vix(SPX_returns)

    SPX_return_values = [return_tuple[1] for return_tuple in SPX_returns]
    VIX_levels = [return_tuple[2] for return_tuple in SPX_VIX]

    bins = int(len(SPX_return_values)**0.33333)

    VIX_max = max(VIX_levels)
    VIX_min = min(VIX_levels)
    VIX_range = VIX_max - VIX_min
    VIX_step = VIX_range / bins
    VIX_intervals = []
    for i in range(bins + 1):
        VIX_intervals.append([VIX_min + VIX_step * i, VIX_min + VIX_step * (i + 1)])

    SPX_interval_values = []
    for v in VIX_intervals:
        interval_values = []
        for i in range(len(SPX_return_values)):
            if v[0] <= VIX_levels[i] < v[1]:
                interval_values.append(SPX_return_values[i])
        SPX_interval_values.append(interval_values)

    print("--" * 30)
    print(bins)
    while True:
        index = int(input("Enter range index: "))
        if 0 <= index < len(VIX_intervals):
            print(SPX_interval_values[index])
            interval_bins = int(len(SPX_interval_values[index])**0.5)
            plt.figure(figsize=(10, 6))
            plt.hist(SPX_interval_values[index], bins=interval_bins, color='blue', edgecolor='black')
            plt.xlabel('SPX Returns (1 month) %')
            plt.ylabel('Frequency')
            plt.title(f'SPX Returns - VIX Interval: {VIX_intervals[index]}')
            plt.grid(True)
            plt.show()
        else:
            break

    # Histogram
    # plt.figure(figsize=(10, 6))
    # plt.hist(SPX_return_values, bins=bins, color='blue', edgecolor='black')
    # plt.xlabel('SPX Returns (1 month) %')
    # plt.ylabel('Frequency')
    # plt.title('SPX Returns')
    # plt.grid(True)
    # plt.show()

    # Dot plot
    # plt.figure(figsize=(10, 6))
    # plt.plot(SPX_return_values, VIX_levels, 'o', color='blue')
    # plt.xlabel('SPX Returns (1 month) %')
    # plt.ylabel('VIX Level')
    # plt.title('SPX Returns vs. VIX Level')
    # plt.grid(True)
    # plt.show()







