from AbstractTradingStrategy import AbstractTradingStrategy
class TradingStrategy:
    def __init__(self):
        self._strategies = {}
        self._current_strategy = None

    def register_strategy(self, name, strategy: AbstractTradingStrategy):
        if not isinstance(strategy, AbstractTradingStrategy):
            raise TypeError("Strategy must inherit from AbstractTradingStrategy.")
        self._strategies[name] = strategy

    def set_strategy(self, name):
        if name not in self._strategies:
            raise ValueError(f"Strategy {name} is not registered.")
        self._current_strategy = self._strategies[name]

    def get_current_strategy(self) -> AbstractTradingStrategy:
        if self._current_strategy is None:
            raise ValueError("No strategy is currently set.")
        return self._current_strategy

    def get_strategy_names(self):
        return list(self._strategies.keys())
    
