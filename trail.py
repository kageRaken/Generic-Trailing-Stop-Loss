import ccxt
from exchange import Exchange
import config
import time


class StopTrail():

    def __init__(self):
        self.exchange = Exchange(
            exchange_id=config.API_DETAILS['EXCHANGE_ID'],
            api_key=config.API_DETAILS['API_KEY'],
            api_secret=config.API_DETAILS['API_SECRET']
        )
        self.order_id = ""
        self.market = config.OPTIONS["SYMBOL"]
        self.type = "sell"
        self.starting_price = float(config.OPTIONS["STARTING_PRICE"])
        self.percentage = float(config.OPTIONS["PERCENTAGE"])
        self.interval = 1
        self.running = False
        self.stoploss = self.initialize_stop()
        self.amount = self.exchange.get_balance(self.market.split("/")[0])

    def initialize_stop(self):
        if self.type == "buy":
            return (self.starting_price * (1 + self.percentage))
        else:
            return (self.starting_price * (1 - self.percentage))

    def update_stop(self):
        price = self.exchange.get_price(self.market)
        self.last_price = price
        if self.type == "sell":
            if (price * (1 - self.percentage)) > self.stoploss:
                self.stoploss = price * (1 - self.percentage)
                self.order_id = self.exchange.sell(self.market, self.amount, self.stoploss, self.order_id)
                print("New high observed: Updating stop loss to %.8f" %
                      self.stoploss)
            elif price <= self.stoploss:
                self.running = False
                print("Sell triggered | Price: %.8f | Stop loss: %.8f | Amount: %.8f" % (
                    price, self.stoploss, self.amount))
        elif self.type == "buy":
            if (price * (1 + self.percentage)) < self.stoploss:
                self.stoploss = price * (1 + self.percentage)
                print("New low observed: Updating stop loss to %.8f" %
                      self.stoploss)
            elif price >= self.stoploss:
                self.running = False
                balance = self.exchange.get_balance(self.market.split("/")[1])
                price = self.exchange.get_price(self.market)
                # 0.10% maker/taker fee without BNB
                amount = (balance / price) * 0.999
                self.exchange.buy(self.market, amount, price)
                print("Buy triggered | Price: %.8f | Stop loss: %.8f" %
                      (price, self.stoploss))

    def print_status(self):
        last = self.exchange.get_price(self.market)
        print("---------------------")
        print("Trail type: %s" % self.type)
        print("Market: %s" % self.market)
        print("Stop loss: %.8f" % self.stoploss)
        print("Last price: %.8f" % last)
        print("Stop size: %.8f" % self.percentage)
        print("---------------------")

    def run(self):
        self.running = True
        while (self.running):
            self.update_stop()
            self.print_status()
            time.sleep(1)
