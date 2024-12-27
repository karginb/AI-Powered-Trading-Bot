from AbstractTradingStrategy import AbstractTradingStrategy

class MomentumStrategy(AbstractTradingStrategy):
    def execute_strategy(self, market_data):
        if market_data[-1] > market_data[-2]:
            return "BUY"
        elif market_data[-1] < market_data[-2]:
            return "SELL"
        else:
            return "HOLD"