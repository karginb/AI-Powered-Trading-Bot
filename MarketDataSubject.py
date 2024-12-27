from abc import ABC, abstractmethod

class MarketDataSubject(ABC):
    @abstractmethod
    def add_observer(self, observer):
        pass
    @abstractmethod
    def remove_observer(self, observer):
        pass
    @abstractmethod
    def notify_observers(self, market_data):
        pass