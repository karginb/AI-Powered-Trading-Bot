from Command import Command
class BuyCommand(Command):
    def __init__(self, asset):
        self.asset = asset
        
    def execute(self, log_callback):
        log_callback(f"Executing BUY order for: {self.asset}")