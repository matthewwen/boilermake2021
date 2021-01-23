from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message
import robin_stocks as r
import os


def order_information(name, symbol, quanity, buy_sell, limit_price, stop_price, timeout_code):
    message = create_simple_message('Company', name)
    message = create_simple_message('Symbol', symbol, embed=message)
    message = create_simple_message('Quantity', quanity, embed=message)
    message = create_simple_message('Buy or Sell', buy_sell, embed=message)
    message = create_simple_message('Limit Price', limit_price, embed=message)
    message = create_simple_message('Stop Price', stop_price, embed=message)
    message = create_simple_message('Timeout Code', timeout_code, embed=message)

    return message


class UserCommandTrade(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)

    async def run(self):
        #r.login(os.getenv('ROBINHOOD_USERNAME'), os.getenv('ROBINHOOD_PASSWORD'))
        stock = self.content.replace('$order ', '').upper().split()
        print(stock)
        name, symbol, quanity, buy_sell, limit_price, stop_price, timeout_code = stock

        message = order_information(name, symbol, quanity, buy_sell, limit_price, stop_price, timeout_code)
        self.response.set_state(True)
        self.response.add_response(message)

        if len(self.response.response) == 0:
            self.response.set_error_response(0)
        self.response.done = True
