import tkinter as tk
from tkinter import ttk
from threading import Thread
from MarketDataProvider import MarketDataProvider
from TradingBot import TradingBot
from MovingAverageStrategy import MovingAverageStrategy
from BollingerBandsStrategy import BollingerBandsStrategy
from MomentumStrategy import MomentumStrategy
from RsiStrategy import RsiStrategy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import queue


class TradingBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Bot with Live Chart")
        self.root.geometry("1280x960")
        self.root.resizable(False, False)

        # Variables
        self.asset = tk.StringVar(value="DOAS.IS")
        self.selected_strategy = tk.StringVar(value="Moving Average")
        self.log_text = tk.StringVar(value="Welcome to Trading Bot!\n")
        self.log_queue = queue.Queue()  # Log Queue
        self.provider = None
        self.bot = None
        self.running = False
        self.market_data = None  # Store fetched market data for plotting

        # Layout
        self.create_widgets()

        # Handle window close event to stop the bot gracefully
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Start Log Queue Process
        self.root.after(100, self.process_log_queue)

    def create_widgets(self):
        # Asset Input
        tk.Label(self.root, text="Asset:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(self.root, textvariable=self.asset).grid(row=0, column=1, padx=10, pady=10)

        # Strategy Selection
        tk.Label(self.root, text="Strategy:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        strategy_menu = ttk.Combobox(
            self.root, textvariable=self.selected_strategy, 
            values=["Moving Average", "Bollinger Bands", "Momentum", "RSI"]
        )
        strategy_menu.grid(row=1, column=1, padx=10, pady=10)

        # Start/Stop Buttons
        self.start_button = tk.Button(self.root, text="Start", command=self.start_bot)
        self.start_button.grid(row=2, column=0, padx=10, pady=10)
        self.stop_button = tk.Button(self.root, text="Stop", state="disabled", command=self.stop_bot)
        self.stop_button.grid(row=2, column=1, padx=10, pady=10)

        # Log Display
        tk.Label(self.root, text="Log:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.log_box = tk.Text(self.root, height=29, width=75)
        self.log_box.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.log_box.insert("end", self.log_text.get())
        self.log_box.config(state="disabled")

        # Matplotlib Chart
        self.figure, self.ax = plt.subplots(figsize=(7, 5))
        self.ax.set_title("Live Stock Price Chart")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Price")
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().grid(row=4, column=2, padx=10, pady=10, rowspan=2)

    def update_log(self, message):
        self.log_queue.put(message)  # Add Message to Queue

    def process_log_queue(self):
        # Updates Messages That In The Log Queue
        while not self.log_queue.empty():
            message = self.log_queue.get()
            self.log_text.set(self.log_text.get() + message + "\n")
            self.log_box.config(state="normal")
            self.log_box.insert("end", message + "\n")
            self.log_box.see("end")
            self.log_box.config(state="disabled")
        
        
        self.root.after(100, self.process_log_queue)

    def start_bot(self):
        if self.running:
            self.update_log("Bot is already running.")
            return

        # Stop any existing provider and reset data
        if self.provider:
            self.provider.stop()
            self.provider.reset()
            self.clear_chart()  

        self.update_log(f"Starting bot for Asset: {self.asset.get()} with strategy: {self.selected_strategy.get()}")

        # Setup Market Data Provider and Bot
        self.provider = MarketDataProvider(
            asset=self.asset.get(),
            log_callback=self.update_log
        )
        strategy = self.get_strategy(self.selected_strategy.get())
        self.bot = TradingBot(self.asset.get(), strategy, self.update_log)
        self.provider.add_observer(self.bot)

        self.running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        # Load market data
        self.provider.load_market_data()
        self.market_data = self.provider.market_data

        # Run the provider in a separate thread to avoid blocking the GUI
        self.bot_thread = Thread(target=self.run_provider, daemon=True)
        self.bot_thread.start()

    def run_provider(self):
        try:
            self.provider.start()
            # Continuously update the chart with new data
            self.update_chart_continuously()
        except Exception as e:
            self.update_log(f"Error: {e}")
            self.stop_bot()

    def stop_bot(self):
        if not self.running:
            self.update_log("Bot is not running.")
            return

        self.update_log("Stopping bot...")
        self.running = False
        self.provider.stop()
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def get_strategy(self, strategy_name):
        if strategy_name == "Moving Average":
            return MovingAverageStrategy()
        elif strategy_name == "Bollinger Bands":
            return BollingerBandsStrategy()
        elif strategy_name == "Momentum":
            return MomentumStrategy()
        elif strategy_name == "RSI":
            return RsiStrategy()
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")

    def update_chart_continuously(self):
        if self.market_data is None or self.market_data.empty:
            return

        # Extract close prices for plotting
        close_prices = self.market_data['Close'].values.tolist()
        times = self.market_data.index.tolist()

        # Update the chart
        self.ax.clear()
        self.ax.plot(times, close_prices, label="Close Price")
        self.ax.set_title(f"Live Stock Price for {self.asset.get()}")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Price")
        self.ax.legend()

        # Refresh canvas
        self.canvas.draw()

        # If the bot is still running, schedule the next update after 1 second
        if self.running:
            self.root.after(1000, self.update_chart_continuously)  # Update every 1 second
    
    def clear_chart(self):
        # Clear the chart for a fresh start.
        self.ax.clear()
        self.ax.set_title("Live Stock Price Chart")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Price")
        self.canvas.draw()

    def on_close(self):
        # Stop the bot and close the application when the window is closed
        if self.running:
            self.stop_bot()
        self.root.quit()  
        
if __name__ == "__main__":
    root = tk.Tk()
    app = TradingBotGUI(root)
    root.mainloop()
