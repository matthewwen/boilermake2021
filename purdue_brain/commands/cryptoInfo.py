from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message
import robin_stocks as r
import os

def crypto_info(name, symbol, price, market, industry):
    message = create_simple_message('Crypto', name)
    message = create_simple_message('Symbol', symbol, embed=message)
    message = create_simple_message('Price per share', '${:,.2f}'.format(float(price)), embed=message)
    message = create_simple_message('Market cap', '${:,.2f}'.format(float(market)), embed=message)
    message = create_simple_message('Industry', industry, embed=message)
    return message


class UserCommandCryptoInfo(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)

    async def run(self):
        r.login(os.getenv('ROBINHOOD_USERNAME'), os.getenv('ROBINHOOD_PASSWORD'))
        crypto = self.content.replace('$crypto_info ', '').upper().split()
        for c in crypto:
            instrumental_data = r.stocks.find_instrument_data(s)
            fund = r.stocks.get_fundamentals(s)

            for d, f in zip(instrumental_data, fund):
                if None in [d, f]:
                    message = "'" + c + "' Crypto symbol doesn't exist."
                    self.response.set_state(False)
                    self.response.add_response(message)
                    continue
                name = d['simple_name']
                symbol = d['symbol']
                price = r.stocks.get_latest_price(symbol)[0]
                details = f['description']
                market = f['market_cap']
                industry = f['industry']

                message = crypto_info(name, symbol, price, market, details, industry, link)
                self.response.set_state(True)
                self.response.add_response(message)

        if len(self.response.response) == 0:
            self.response.set_error_response(0)
        self.response.done = True
