import ccxt

class Exchange():

    def __init__(self, exchange_id, api_key, api_secret):
        exchange_class = getattr(ccxt, exchange_id)
        self.ccxtClient = exchange_class({
            'apiKey': api_key,
            'secret': api_secret,
            'timeout': 30000,
            'enableRateLimit': True
        })

    def buy(self, market, amount, price):
        return 0
        '''return (self.ccxtClient.create_order(
            symbol=market,
            type="limit",
            side="buy",
            amount=amount,
            price=price,
        ))'''

    def sell(self, market, amount, price, old_order_id):
        if old_order_id != "":
            self.ccxtClient.cancel_order(old_order_id)
        order = self.ccxtClient.create_order(
            symbol=market,
            type="stop-loss",
            side="sell",
            amount=amount,
            price=price,
            params={'ordertype': 'stop-loss'}
        )

        return order["id"]
    


    def get_price(self, market):
        return float(self.ccxtClient.fetch_ticker(market)['last'])

    def get_balance(self, coin):
        return float(self.ccxtClient.fetch_balance()[coin]['total'])
