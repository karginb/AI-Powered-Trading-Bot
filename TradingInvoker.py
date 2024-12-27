class TradingInvoker:
    def __init__(self, log_callback):
        self.command = None
        self.log_callback = log_callback


    def set_command(self, command):
        self.command = command

    def execute_command(self):
        self.command.execute(self.log_callback)