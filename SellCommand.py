from Command import Command
class SellCommand(Command):
    def __init__(self, asset):
        self.asset = asset

    def execute(self, log_callback):
        log_callback(f"Executing SELL order for: {self.asset}")
    