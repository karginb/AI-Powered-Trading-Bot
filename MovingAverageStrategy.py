from AbstractTradingStrategy import AbstractTradingStrategy

class MovingAverageStrategy(AbstractTradingStrategy):
    def __init__(self, short_window=3, long_window=5):
        self.short_window = short_window
        self.long_window = long_window

    def execute_strategy(self, market_data):
        if len(market_data) < self.long_window:
            return "HOLD"

        short_ma = self.calculate_moving_average(market_data, self.short_window)
        long_ma = self.calculate_moving_average(market_data, self.long_window)

        if short_ma > long_ma:
            return "BUY"
        elif short_ma < long_ma:
            return "SELL"
        else:
            return "HOLD"

    def calculate_moving_average(self, data, window):
        return sum(data[-window:][0]) / window