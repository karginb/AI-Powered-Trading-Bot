from abc import ABC, abstractmethod

class AbstractTradingStrategy(ABC):
    def decide(self, market_data):
        if not self._is_valid_data(market_data):
            return "HOLD"
        return self.execute_strategy(market_data)

    def _is_valid_data(self, market_data):
        return market_data and len(market_data) > 1

    @abstractmethod
    def execute_strategy(self, market_data):
        pass