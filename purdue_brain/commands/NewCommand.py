from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message
from purdue_brain.wrappers.discord_wrapper import DiscordWrapper


class UserCommandNewCommand(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)

    async def run(self):
        print(DiscordWrapper.fire.get_user(self.author.id))
        DiscordWrapper.fire.set_property('bitch', self.author.id, 'corevette corvette')
        message = create_simple_message("Suhanan", "Says Hello")
        self.response.add_response(message, True)
