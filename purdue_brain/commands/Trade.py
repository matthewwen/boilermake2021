from robin_stocks.robin_stocks import robin_stocks

from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message
import robin_stocks as r
import os


def order_information(name, symbol, quantity, buy_sell, limit_price, stop_price, timeout_code):
    message = create_simple_message('Company', name)
    message = create_simple_message('Symbol', symbol, embed=message)
    message = create_simple_message('Quantity', quantity, embed=message)
    message = create_simple_message('Buy or Sell', buy_sell, embed=message)
    message = create_simple_message('Limit Price', limit_price, embed=message)
    message = create_simple_message('Stop Price', stop_price, embed=message)
    message = create_simple_message('Timeout Code', timeout_code, embed=message)

    return message


class UserCommandTrade(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)

    async def run(self):
        r.login(os.getenv('ROBINHOOD_USERNAME'), os.getenv('ROBINHOOD_PASSWORD'))

        if '$order ' in self.content:
            stock = self.content.replace('$order ', '').upper().split()
            name, symbol, quantity, buy_sell, limit_price, stop_price, timeout_code = stock
            #confirmation = r.order(str(symbol), int(quantity), str(buy_sell), float(limit_price), float(stop_price), str(timeout_code))
            confirmation = r.order('AZRX', 1, 'buy', 1.80, 1.80, 'gfd')

        elif '$order_buy_market ' in self.content:
            stock = self.content.replace('$order_buy_market ', '').upper().split()
            name, symbol, quantity, timeout_code = stock
            #confirmation = r.order_buy_market(str(symbol), int(quantity), str(timeout_code))
            confirmation = r.order_buy_market('AZRX', 1)
            print(confirmation)

        elif '$order_sell_market ' in self.content:
            stock = self.content.replace('$order_sell_market ', '').upper().split()
            name, symbol, quantity, buy_sell, limit_price, stop_price, timeout_code = stock
            confirmation = r.order_sell_market(str(symbol), int(quantity), str(buy_sell), float(limit_price), float(stop_price), str(timeout_code))

        elif '$order_buy_limit ' in self.content:
            stock = self.content.replace('$order_buy_limit ', '').upper().split()
            name, symbol, quantity, limit_price, timeout_code = stock
            confirmation = r.order_buy_limit(str(symbol), int(quantity), float(limit_price), str(timeout_code))

        elif '$order_sell_limit ' in self.content:
            stock = self.content.replace('$order_sell_limit ', '').upper().split()
            name, symbol, quantity, limit_price, timeout_code = stock
            confirmation = r.order_sell_limit(str(symbol), int(quantity), float(limit_price), str(timeout_code))

        elif '$order_buy_stop_loss ' in self.content:
            stock = self.content.replace('$order_buy_stop_loss ', '').upper().split()
            name, symbol, quantity, stop_price, timeout_code = stock
            confirmation = r.order_buy_stop_loss(str(symbol), int(quantity), float(stop_price), str(timeout_code))

        elif '$order_sell_stop_loss ' in self.content:
            stock = self.content.replace('$order_sell_stop_loss ', '').upper().split()
            name, symbol, quantity, stop_price, timeout_code = stock
            confirmation = r.order_sell_stop_loss(str(symbol), int(quantity), float(stop_price), str(timeout_code))

        elif '$order_buy_trailing_stop ' in self.content:
            stock = self.content.replace('$order_buy_trailing_stop ', '').upper().split()
            name, symbol, quantity, buy_sell, limit_price, stop_price, timeout_code = stock
            confirmation = r.order_buy_trailing_stop(str(symbol), int(quantity), str(buy_sell), float(limit_price), float(stop_price),
                               str(timeout_code))

        elif '$order_sell_trailing_stop ' in self.content:
            stock = self.content.replace('$order_sell_trailing_stop ', '').upper().split()
            name, symbol, quantity, trailAmount, trailType, timeout_code = stock
            confirmation = r.order_sell_trailing_stop(str(symbol), int(quantity), float(trailAmount), str(trailType), str(timeout_code))

        elif '$order_trailing_stop ' in self.content:
            stock = self.content.replace('$order_trailing_stop ', '').upper().split()
            name, symbol, quantity, buy_sell, trailingAmount, trailType, timeout_code = stock
            confirmation = r.order_trailing_stop(str(symbol), int(quantity), str(buy_sell), float(trailingAmount), str(trailType),
                                   str(timeout_code))

        elif '$order_sell_stop_limit ' in self.content:
            stock = self.content.replace('$order_sell_stop_limit ', '').upper().split()
            name, symbol, quantity, limit_price, stop_price, timeout_code = stock
            confirmation = r.order_sell_stop_limit(str(symbol), int(quantity), float(limit_price), float(stop_price), str(timeout_code))

        message = order_information(name, symbol, quantity, buy_sell=None, limit_price=None, stop_price=None, timeout_code=None)
        self.response.set_state(True)
        #self.response.add_response(confirmation)
        self.response.add_response(message)

        if len(self.response.response) == 0:
            self.response.set_error_response(0)
        self.response.done = True
