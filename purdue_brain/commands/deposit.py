from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message
import robin_stocks as r
import os


class UserCommandDeposit(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)

    async def run(self):
        r.login(os.getenv('ROBINHOOD_USERNAME'), os.getenv('ROBINHOOD_PASSWORD'))
        args = self.content.replace('$deposit ', '').upper()
        details = r.account.get_linked_bank_accounts()
        for d in details:
            if os.getenv('CONNECT') == 'True':
                listDict = r.account.deposit_funds_to_robinhood_account(d['url'], args)
                try:
                    message = 'Transaction successful: ' + '${:,.2f}'.format(float(listDict['amount'])) + ' is currently ' + listDict['state']
                    self.response.set_state(True)
                except:
                    message = 'Transaction unsuccessful.'
                    self.response.set_state(False)
            else:
                listDict = r.account.deposit_funds_to_robinhood_account(d['url'], 0.01)
                try:
                    message = 'Transaction successful: ' + '${:,.2f}'.format(float(100)) + ' is currently ' + listDict['state']
                    self.response.set_state(True)
                except:
                    message = 'Transaction unsuccessful.'
                    self.response.set_state(False)
        self.response.add_response(message)

        if len(self.response.response) == 0:
            self.response.set_error_response(0)
        self.response.done = True
