from abc import ABC, abstractmethod
class MarketDataObserver(ABC):
    @abstractmethod
    def on_market_data_update(self, market_data):
        pass