from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message
import robin_stocks as r
import os

class UserCommandTradeHelp(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)

    async def run(self):
        message = create_simple_message('$trade_help', 'Gives a brief description of each command')
        message = create_simple_message('$order [SYMBOL] [QUANTITY] ["BUY" OR "SELL"] [LIMIT PRICE] [STOP PRICE] [TIMEOUT CODE]', '‘Timeout codes: gtc’ = good until cancelled.‘gfd’ = good for the day.‘ioc’ = immediate or cancel.‘opg’ execute at opening.', embed=message)

        self.response.set_state(True)
        self.response.add_response(message)

        if len(self.response.response) == 0:
            self.response.set_error_response(0)
        self.response.done = True
