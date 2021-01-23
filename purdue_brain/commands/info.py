from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message
import robin_stocks as r
import os

class UserCommandInfo(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)
        print(content)

    async def run(self):
        r.login(os.getenv('ROBINHOOD_USERNAME'), os.getenv('ROBINHOOD_PASSWORD'))
        stock = self.content.replace('$info ', '').upper()
        dict = r.stocks.find_instrument_data(stock)
        for d in dict:
            name = d['simple_name']
            symbol = d['symbol']
            price = r.stocks.get_latest_price(symbol)[0]
            tradability = d['tradability']
            link = 'https://robinhood.com/stocks/' + symbol
        fund = r.stocks.get_fundamentals(stock)
        for d in fund:
            details = d['description']
            market = d['market_cap']
            industry = d['industry']

        message = create_simple_message('Company', name)
        message = create_simple_message('Symbol', symbol, embed=message)
        message = create_simple_message('Price per share', '${:,.2f}'.format(float(price)), embed=message)
        message = create_simple_message('Market cap', '${:,.2f}'.format(float(market)), embed=message)
        message = create_simple_message('About', details, embed=message)
        message = create_simple_message('Industry', industry, embed=message)
        message = create_simple_message('More info', link, embed=message)
        self.response.add_response(message, True)
