from AbstractTradingStrategy import AbstractTradingStrategy
import numpy as np

class BollingerBandsStrategy(AbstractTradingStrategy):
    def execute_strategy(self, market_data):
        mean = self.calculate_mean(market_data)
        std_dev = self.calculate_standard_deviation(market_data, mean)

        upper_band = mean + 2 * std_dev
        lower_band = mean - 2 * std_dev

        last_price = market_data[-1]

        if last_price > upper_band:
            return "SELL"  # Overbought
        elif last_price < lower_band:
            return "BUY"  # Oversold
        else:
            return "HOLD"

    def calculate_mean(self, data):
        return np.mean(data)

    def calculate_standard_deviation(self, data, mean):
        return np.std(data)