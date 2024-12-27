from AbstractTradingStrategy import AbstractTradingStrategy

class RsiStrategy(AbstractTradingStrategy):
    def execute_strategy(self, market_data):
        rsi = self._calculate_rsi(market_data)
        if rsi < 30:
            return "BUY"
        elif rsi > 70:
            return "SELL"
        else:
            return "HOLD"

    def _calculate_rsi(self, market_data):
        gains = losses = 0
        for i in range(1, len(market_data)):
            diff = market_data[i][0] - market_data[i - 1][0]
            if diff > 0:
                gains += diff
            else:
                losses -= diff
        if losses == 0:
            return 100
        rs = gains / losses
        return 100 - (100 / (1 + rs))