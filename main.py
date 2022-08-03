import re
import discord
import os
import dotenv 

#load env flags
dotenv.load_dotenv()


scare_flag = False
usertag_flag = False
debug = bool(os.getenv('DEBUG'))
bot_token = os.getenv('DISCORD_TOKEN')


class bot_return_struct:
    def __init__(self, string, userflag):
        self.string = string
        self.userflag = userflag
    def rtr_resp(self):
        return self.string
    def rtr_flag(self):
        return self.userflag

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
        p2 = reply_bot_message(self, message)
        p3 = p2.rtr_resp()
        p4 = p2.rtr_flag()
        await message.reply(p3, mention_author=p4)
        await message.add_reaction(emoji ='🇫')





def reply_bot_message(self, message):
    bot_reply = ''
    global scare_flag
    global usertag_flag
    usertag_flag = False
    action_flag = 0
    if debug == True:
        print('processing {0.author}: {0.content} '.format(message))
        
    #alis for cleaner reading
    intake = message.content

    if intake.isupper():
        bot_reply = bot_reply + 'Please stop yelling at me its scawwy but '
        usertag_flag = True
        scare_flag = True
    else:
        if scare_flag == True:
                bot_reply = bot_reply + 'Thankies and '
                if debug == True:
                    print("trip thank flag")
                scare_flag = False

    intake = message.content.lower()
    if intake.startswith('hello'):
        bot_reply = bot_reply + 'Hello!'
        action_flag = 1
    elif intake.startswith('googlefu') or intake.startswith('can the internet tell me why'):
        if intake.startswith('can the internet tell me why'):
            proc1 = re.search("(?<=can the internet tell me why ).*",intake)
        else:
            proc1 = re.search("(?<=googlefu ).*",intake)
            bot_reply = bot_reply + 'https://www.google.com/search?q='+str(proc1[0]).replace(' ','+')
        action_flag = 1

    #failsale flag to return custom message, not needed but nice 
    if action_flag == 1:
        if debug == True:
            print("tried sending message: -" + str(bot_reply) + '- with UT_flag: -' + str(usertag_flag) +'-')
        return bot_return_struct(bot_reply, usertag_flag)
    #failsafe return false
    return False


client = MyClient()
client.run(bot_token)
