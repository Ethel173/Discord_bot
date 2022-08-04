import discord
import os
import dotenv 
from bot_message_handler import check_message_processor

#load env flags
dotenv.load_dotenv()
debug = bool(os.getenv('DEBUG'))
bot_token = os.getenv('DISCORD_TOKEN')

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as = ' +str(self.user.name))
        print('with userid = ' + str(self.user.id))
        print('------')
        await client.change_presence(status=discord.Status.online, activity=discord.Game("in a dev console"))

    async def on_message(self, message):
        if debug == True:
            print('caught message: {0.author}: {0.content}'.format(message))
        #prevent replies and logging of bot
        if message.author.id == self.user.id:
            if debug == True:
                print('discarded self-message: {0.author}: {0.content}'.format(message))
            return
        p2 = check_message_processor(self, message)
        if debug == True:
            print('p2 = ',p2)
        if p2 == False:
            if debug == True:
                print('no reply sent')
            return
        else:
            await message.reply(p2.rtr_resp(), mention_author=p2.rtr_flag())
        #await message.add_reaction(emoji ='🇫')




client = MyClient()
client.run(bot_token)
