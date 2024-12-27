from MarketDataObserver import MarketDataObserver
from TradingInvoker import TradingInvoker
from BuyCommand import BuyCommand
from SellCommand import SellCommand
from HoldCommand import HoldCommand

class TradingBot(MarketDataObserver):
    def __init__(self, asset, strategy, log_callback):
        self.asset = asset
        self.strategy = strategy
        self.invoker = TradingInvoker(log_callback)

    def set_strategy(self, strategy):
        self.strategy = strategy

    def on_market_data_update(self, market_data):
        decision = self.strategy.decide(market_data)

        if decision == "BUY":
            command = BuyCommand(self.asset)
        elif decision == "SELL":
            command = SellCommand(self.asset)
        else:
            command = HoldCommand()

        self.invoker.set_command(command)
        self.invoker.execute_command()