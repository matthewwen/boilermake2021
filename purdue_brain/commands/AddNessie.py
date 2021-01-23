from purdue_brain.feature.nessie import Nessie
from purdue_brain.wrappers.discord_wrapper import DiscordWrapper
from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message


class UserAddApiKey(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)

    def create_customer_and_user(self):
        nessie_property = DiscordWrapper.fire.get_property('nessie_customer_id', self.author.id, None)
        if nessie_property is None:
            nessie = Nessie(None, None)
            response = nessie.create_customer() and nessie.create_account()
            DiscordWrapper.fire.set_property('nessie_customer_id', self.author.id,
                                             {'customer_id': nessie.customer_id, 'account_id': nessie.account_id})
            return response
        else:
            return False

    async def run(self):
        response = self.create_customer_and_user()
        if response:
            message = create_simple_message('Added Account', 'Successfully Added Key to Profile')
            self.response.add_response(message, True)
            self.response.done = True
        else:
            message = create_simple_message('Error', 'You already connected a bank account.')
            self.response.add_response(message, False)
            self.response.set_state(False, done=True)


class GetAccountInfo(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)
