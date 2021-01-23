from purdue_brain.feature.nessie import Nessie
from purdue_brain.wrappers.discord_wrapper import DiscordWrapper
from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message

import requests
import json


class UserGetApiLink(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)

    async def run(self):
        link = "http://api.nessieisreal.com/"
        profile_link = link + "/profile"
        message = create_simple_message('Get Bank Key Here',
                                        f'1. Click on This {link}\n'
                                        '2. Login with GitHub\n'
                                        f'3. Click on this {profile_link}'
                                        ' and it should display your Api Key.\n'
                                        '4. Add Bank Key by typing \'$add_bank_key [key]\''
                                        )
        self.response.set_state(True)
        self.response.add_response(message, True)
        self.response.done = True
        pass


class UserAddApiKey(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)

    def add_api_key(self):
        stock = self.content.replace('$add_bank_key ', '')
        DiscordWrapper.fire.set_property('bankKey', self.author.id, stock)
        nessie = Nessie(self.author.id, stock)
        return nessie.create_customer() and nessie.create_account()

    async def run(self):
        response = self.add_api_key()
        if response:
            message = create_simple_message('Added Key', 'Successfully Added Key to Profile')
            self.response.add_response(message)
            self.response.add_response(message, True)
            self.response.done = True
        else:
            self.response.set_error_response(0, True)


class GetAccountInfo(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)
