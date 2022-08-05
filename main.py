import re
import sys
import discord
from envflags import client_id,guild_id,bot_token,debug,home_channel
from utils import roll_random_in_array,psudo_list_rng
#has to be up here for debug assignment
#pythons built in bool(X) doesnt convert 'False' into False
def str_to_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        sys.exit("invalid debug asisgnment in .env")
debug = str_to_bool(debug)
#globals
scare_flag = False
yell_at_user_flag = False
current_game = ''

#editable flavor text
startup_statuses = ['crying over RNG','with the dev console','crashing this bot with no error logs','gao']
#make sure to add in the ' ' for proper formatting for below
google_search_keywords = ['googlefu ','can the internet tell me why ' ,'explain to me ']
scared_responses = ['Please stop yelling at me its scawwy but ','Loud Noises scawwy but ','AAAHH ','awwwww you made me spill my drink ']
un_scared_response = ['Thankies and ','thankuus ','ehe ']
RNG_like_dislike = ['i hate ','i love ','i dont really like ','i enjoy ']


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
        global current_game
        print('Logged in as = ' +str(self.user.name))
        print('with userid = ' + str(self.user.id))
        print('------')
        current_game = roll_random_in_array(startup_statuses)
        await client.change_presence(status=discord.Status.online, activity=discord.Game(current_game))

        if home_channel != False:
            channel = client.get_channel(home_channel)
            if debug == True:
                print('tried mentioning startup in channel :', channel)
            await channel.send("bot online")

    async def on_message(self, message):
        #prevent replies and logging of bot
        if message.author.id == self.user.id:
            if debug == True:
                print('discarded self-message: {0.author}: {0.content}'.format(message))
                #print(str(message.channel.id))
            return
        global current_game
        #aliases
        chanel_id = message.channel
        intake = message.content
        intake_lower = intake.lower()
        command_match = ''
        #this is used later despite VS saying otherwise
        googlestorage = ''
        #debug
        if debug == True:
            print('caught message: {0.author}: {0.content}'.format(message))

        #start logic
        if message.content.startswith('hey gura change your game'):
            await chanel_id.send("im trying ok")
            psudo_rng = psudo_list_rng(startup_statuses,current_game)
            psudo_change_game = roll_random_in_array(psudo_rng)
            await client.change_presence(status=discord.Status.online, activity=discord.Game(psudo_change_game))
        elif intake_lower.startswith('hello'):
            command_match = 'hw'
        elif intake_lower.startswith('hey gura what do you think of '):
            command_match = 'rng_like'
        elif start_keyword_in_arr(intake_lower, google_search_keywords):
            command_match = 'googlefu'
        elif intake_lower.startswith('source me'):
            command_match='source'
        if command_match != '':
            p2 = reply_bot_message(self, message, command_match)
            if debug == True:
                print('p2 = ',p2)
            if p2 != False:
                await message.reply(p2.rtr_resp(), mention_author=p2.rtr_flag())

    async def on_message_delete(self,message):
        if message.author.id == self.user.id:
            return
        else:
            channel = client.get_channel(message.channel.id)
            await channel.send("i saw that")

        #TODO / commands
        #await message.add_reaction(emoji ='🇫')


#self arg unused but may be used in future
def reply_bot_message(self, message, command):
    bot_reply = ''
    global scare_flag
    global yell_at_user_flag
    yell_at_user_flag = False
    if debug == True:
        print('processing {0.author}: {0.content} '.format(message))
    #alis for cleaner reading
    #intake = original conent(used in scare flag), lower for handling logic
    intake = message.content
    intake_lower = intake.lower()
    
    match command:
        case 'hw':
            bot_reply = bot_reply + 'Hello!'
        case 'rng_like':
            proc1 = intake_lower.replace('hey gura what do you think of ','')
            bot_reply = roll_random_in_array(RNG_like_dislike) + proc1
        case 'googlefu':
            bot_reply = bot_reply + 'https://www.google.com/search?q='+str(googlestorage).replace(' ','+')
        case 'source':
            attachemnt_number = len(message.attachments)
            if attachemnt_number == 0:
                return False
            for i in range(0,attachemnt_number):
                url =str(message.attachments[i-1].url)
                pixiv = re.search('\d+(?=_p\d+\.?\_?)',url)
                if pixiv:
                    hunt  = pixiv[0]
                    bot_reply = bot_reply + 'i think this might be a pixiv image\n' + 'https://www.pixiv.net/en/artworks/'+str(hunt)+'\n'
                else:
                    hunt = url.replace('http://','').replace('https://','')
                    bot_reply = bot_reply + 'am dumm, so heres google\n' +'https://www.google.com/searchbyimage?image_url='+str(hunt)+'\n'



    if command != '':
        #'yelling' flavor text in here to only process scare flags if actually responding to comething
        #uses intake as alias for original message
        if intake.isupper():
            bot_reply = roll_random_in_array(scared_responses) + bot_reply
            yell_at_user_flag = True
            scare_flag = True
        else:
            if scare_flag == True:
                    bot_reply = roll_random_in_array(un_scared_response) + bot_reply
                    if debug == True:
                        print("trip thank flag")
                    scare_flag = False

        if debug == True:
            print("tried sending message: -" + str(bot_reply) + '- with UT_flag: -' + str(yell_at_user_flag) +'-')
        return bot_return_struct(bot_reply, yell_at_user_flag)
    #failsafe return false
    return False

def start_keyword_in_arr(input, search_arr):
    global googlestorage
    for i in search_arr:
        #debug if this loop works properly
        if debug == True:
            print('checking for ',i)
        if input.startswith(str(i)):
            googlestorage = input.lower().replace(str(i),'')
            return True



client = MyClient()
def starttime():
    client.run(bot_token)


if __name__ == "__main__":
    starttime()