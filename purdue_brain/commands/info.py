from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message
import robin_stocks as r
import os


def company_stock_info(name, symbol, price, market, details, industry, link):
    message = create_simple_message('Company', name)
    message = create_simple_message('Symbol', symbol, embed=message)
    message = create_simple_message('Market cap', '${:,.2f}'.format(float(market)), embed=message)
    message = create_simple_message('About', details, embed=message)
    message = create_simple_message('Industry', industry, embed=message)
    message = create_simple_message('More info', link, embed=message)
    return create_simple_message('Price per share', '${:,.2f}'.format(float(price)), embed=message)


class UserCommandInfo(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)
        print(content)

    async def run(self):
        r.login(os.getenv('ROBINHOOD_USERNAME'), os.getenv('ROBINHOOD_PASSWORD'))
        stock = self.content.replace('$info ', '').upper()
        dict = r.stocks.find_instrument_data(stock)
        fund = r.stocks.get_fundamentals(stock)

        for d, f in zip(dict, fund):
            if None in [d, f]:
                continue
            name = d['simple_name']
            symbol = d['symbol']
            price = r.stocks.get_latest_price(symbol)[0]
            link = 'https://robinhood.com/stocks/' + symbol

            details = f['description']
            market = f['market_cap']
            industry = f['industry']

            message = company_stock_info(name, symbol, price, market, details, industry, link)
            self.response.set_state(True)
            self.response.add_response(message)
        if not self.response.done:
            self.response.set_error_response(0)
        self.response.done = True
