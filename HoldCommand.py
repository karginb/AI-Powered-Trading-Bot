from Command import Command
class HoldCommand(Command):
    def execute(self, log_callback):
        log_callback("No action taken. HOLD.")
    