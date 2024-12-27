import yfinance as yf
import time
from pandas import DataFrame
from MarketDataSubject import MarketDataSubject

class MarketDataProvider(MarketDataSubject):
    def __init__(self, asset, interval=5, period="1d", data_interval="1m", log_callback=None):
        self.asset = asset
        self.interval = interval
        self.period = period
        self.data_interval = data_interval
        self.market_data: DataFrame | None = None
        self.observers = []
        self.running = False
        self.log_callback = log_callback

    def log(self, message):
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, market_data):
        for observer in self.observers:
            observer.on_market_data_update(market_data)

    def fetch_asset_data(self):
        try:
            self.log(f"Fetching data for {self.asset}...")
            data = yf.download(tickers=self.asset, period=self.period, interval=self.data_interval)
            if data.empty:
                self.log(f"No data found for {self.asset}.")
                return None
            self.log(f"Data fetched successfully for {self.asset}.")
            return data
        except Exception as e:
            self.log(f"Error fetching data for {self.asset}: {e}")
            return None

    def load_market_data(self):
        self.market_data = self.fetch_asset_data()
        if self.market_data is not None:
            self.log(f"Loaded market data for {self.asset}.")
        else:
            self.log(f"Failed to load market data for {self.asset}.")

    def start(self):
        self.running = True
        if self.market_data is None or self.market_data.empty:
            self.log("No market data to process.")
            return
        for index in range(len(self.market_data)):
            if not self.running:
                break
            row = self.market_data.iloc[index]
            price_history = self.market_data['Close'].iloc[:index + 1].values.tolist() 
            self.log(f"Simulated Update: {row.name} - Close: {row['Close']}")
            self.notify_observers(price_history)

            time.sleep(self.interval)
    
    def reset(self):
        self.market_data = None
        self.observers = []
        self.running = False
        self.log("Market data provider has been reset.")

    def stop(self):
        self.running = False
        if self.log_callback:
            self.log("Market data streaming stopped.")