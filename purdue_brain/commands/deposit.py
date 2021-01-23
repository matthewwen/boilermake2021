from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message
import robin_stocks as r
import os


class UserCommandDeposit(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)

    def parse_transaction(self, args, display_arg, d):
        list_dict = r.account.deposit_funds_to_robinhood_account(d['url'], args)
        did_perform = True
        try:
            message = 'Transaction successful: ' + '${:,.2f}'.format(display_arg) + ' is currently ' + list_dict[
                'state']
            self.response.set_state(True)
        except:
            did_perform = False
            message = 'Transaction unsuccessful.'
            self.response.set_state(False)
        return did_perform, message

    async def run(self):
        r.login(os.getenv('ROBINHOOD_USERNAME'), os.getenv('ROBINHOOD_PASSWORD'))
        args = self.content.replace('$deposit ', '').upper()
        details = r.account.get_linked_bank_accounts()
        for d in details:
            args = float(args)
            if args <= 0 or args > 500:
                message = "Transaction failed: Amount is too much"
                successful = False
            elif os.getenv('CONNECT') == 'True':
                message, successful = self.parse_transaction(args, args, d)
            else:
                message, successful = self.parse_transaction(0.01, args, d)
            self.response.add_response(message)

        if len(self.response.response) == 0:
            self.response.set_error_response(0)
        self.response.done = True
