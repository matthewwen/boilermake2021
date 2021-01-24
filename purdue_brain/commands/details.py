from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message
import robin_stocks as r
import os

def findEquity(market_value, crypto, total_equity):
    message = create_simple_message('Total Equity', '${:,.2f}'.format(float(total_equity)))
    message = create_simple_message('Stock Value', '${:,.2f}'.format(float(market_value)), embed=message)
    message = create_simple_message('Crypto Value', '${:,.2f}'.format(float(crypto)), embed=message)
    return message


class UserCommandDetails(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)

    async def run(self):
        r.login(os.getenv('ROBINHOOD_USERNAME'), os.getenv('ROBINHOOD_PASSWORD'))
        profile = r.account.load_phoenix_account()
        # print(profile)
        for p in [profile]:
            for l in [p['equities']]:
                for j in [l['market_value']]:
                    market_value = j['amount']
                    # print(j['amount'])
            for l in [p['total_equity']]:
                equity = l['amount']
                # print(l['amount'])
            for l in [p['crypto']]:
                for j in [l['market_value']]:
                    crypto_value = j['amount']
                    # print(j['amount'])


            message = findEquity(market_value, crypto_value, equity)
            self.response.add_response(message)

        if len(self.response.response) == 0:
            self.response.set_error_response(0)
        self.response.done = True
