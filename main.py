import csv
from fileinput import close
import os
import re
import sys
import discord
from envflags import bot_id,bot_token,debug,home_channel
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
bot_reply = ''
cmd_list=[]
flag_scare = False
flag_ping_user = False
#editable flavor text
startup_statuses = ['crying over RNG','with the dev console','crashing this bot with no error logs','gao']
startup_status_current = ''


class bot_return_struct:
    def __init__(self, string, userflag):
        self.string = string
        self.userflag = userflag
    def rtr_resp(self):
        return self.string
    def rtr_flag(self):
        return self.userflag


class command_no_promt_builder:
    def __init__(self, cmd_name, cmd_payload, cmd_trigger, cmd_desc=''):
        self.cmd_name = cmd_name
        self.cmd_case = cmd_payload
        self.cmd_trigger = cmd_trigger
        self.cmd_desc = cmd_desc
    def rtr_name(self):
        return self.cmd_name
    def rtr_payload(self):
        return self.cmd_case
    def rtr_trigger(self):
        return self.cmd_trigger
    def rtr_desc(self):
        return self.cmd_desc


class MyClient(discord.Client):
    async def on_ready(self):
        global startup_status_current
        #build commands
        cmd_builder()
        print('Logged in as = ' +str(self.user.name))
        print('with userid = ' + str(bot_id))
        print('------')
        startup_status_current = roll_random_in_array(startup_statuses)
        await client.change_presence(status=discord.Status.online, activity=discord.Game(startup_status_current))
        if home_channel != False:
            #channel = client.get_channel(home_channel)
            if debug == True:
                print('tried mentioning startup in channel :', client.get_channel(home_channel))
            await client.get_channel(home_channel).send("bot online")



    async def on_message(self, message):
        #prevent replies and logging of bot messages
        if message.author.id == self.user.id:
            if debug == True:
                print('discarded self-message: {0.author}: {0.content}'.format(message))
            return
        global startup_status_current
        #abort if cant send messages
        #bot_perms_in_channel = get_bot_perms(message)
        if get_bot_perms(message).send_messages == False:
            return
        #debug
        if debug == True:
            print('caught message: {0.author}: {0.content}'.format(message))

        #start logic
        #chat events that return a response
        for cmd in range(len(cmd_list)):
            if type(cmd_list[cmd].rtr_trigger()) != list:
                if re.match(cmd_list[cmd].rtr_trigger(),message.content.lower()):
                    if get_bot_perms(message).send_messages == False:
                        return
                    p2 = reply_bot_message(message, cmd_list[cmd].rtr_payload())
                    if p2 != False and p2.rtr_resp()!="":
                        await message.reply(p2.rtr_resp(), mention_author=p2.rtr_flag())
                    break
            else:
                for i in range(0,len(cmd_list[cmd].rtr_trigger())):
                    if re.match(cmd_list[cmd].rtr_trigger()[i],message.content.lower()):
                        p2 = reply_bot_message(message, cmd_list[cmd].rtr_payload(),cmd_list[cmd].rtr_trigger()[i])
                        if p2 != False and p2.rtr_resp()!="":
                            await message.reply(p2.rtr_resp(), mention_author=p2.rtr_flag())
                        break

    async def on_message_delete(self,message):
        if message.author.id == bot_id:
            return
            #dont fire in DMs
        elif message.channel.type.value != 1:
            channel = client.get_channel(message.channel.id)
            await channel.send("i saw that")


def reply_bot_message(message, command,regex = ''):
    global bot_reply
    global flag_scare
    global flag_ping_user
    if debug == True:
        print('processing {0.author}: {0.content} '.format(message))
    #clear it for new response
    bot_reply = ''
    #make sure to add in the ' ' for proper formatting for below
    scared_responses = ['Please stop yelling at me its scawwy but ','Loud Noises scawwy but ','AAAHH ','awwwww you made me spill my drink ']
    un_scared_response = ['Thankies and ','thankuus ','ehe ']
    RNG_like_dislike = ['i hate ','i love ','i dont really like ','i enjoy ']
    #disabled for next major rewrite
    def change_game():
        global bot_reply
        bot_reply = "im trying ok"
        psudo_rng = psudo_list_rng(startup_statuses,startup_status_current)
        psudo_change_game = roll_random_in_array(psudo_rng)
        change_game(psudo_rng)
    def hw():
        global bot_reply
        bot_reply = 'Hello!'
    def rng_like(message):
        global bot_reply
        proc1 = message.content.lower().replace('hey gura what do you think of ','')
        bot_reply = roll_random_in_array(RNG_like_dislike) + proc1
    def search(message):
        global bot_reply
        proc1 = message.content.lower().replace(regex,'')
        bot_reply = 'https://www.google.com/search?q='+proc1.replace(' ','+')    
    def purge(message):
        mass_del(message.content.lower().replace('purge ',''), message)
    def source(message):
        global bot_reply
        if len(message.attachments) == 0:
            return False
        for i in range(0,len(message.attachments)):
            pixiv = re.search('\d+(?=_p\d+\.?\_?)',str(message.attachments[i-1].url))
            if pixiv:
                hunt  = pixiv[0]
                bot_reply = bot_reply + 'i think this might be a pixiv image\n' + 'https://www.pixiv.net/en/artworks/'+str(hunt)+'\n'
            else:
                hunt = str(message.attachments[i-1].url).replace('http://','').replace('https://','')
                bot_reply = bot_reply + 'am dumm, so heres google\n' +'https://www.google.com/searchbyimage?image_url='+str(hunt)+'\n'
    eval(command+"()")
    if message.content.isupper():
        bot_reply = roll_random_in_array(scared_responses) + bot_reply
        flag_ping_user = True
        flag_scare = True
    else:
        if flag_scare == True:
                bot_reply = roll_random_in_array(un_scared_response) + bot_reply
                '''if debug == True:
                    print("trip thank flag")'''
                flag_scare = False
    if debug == True:
        print("tried sending message: -" + str(bot_reply) + '- with yell_flag: -' + str(flag_ping_user) +'-')
    return bot_return_struct(bot_reply, flag_ping_user)

async def mass_del(number, message):
    try:
        limit_a = int(number)
        if limit_a <= 1:
            raise TypeError
    except TypeError:
            await message.reply('thats not a good number dummy, needs to be 2 or bigger', mention_author=1)
            return
    #DMS or private groups
    if message.channel.type.value == 1:
        async for A in message.channel.history(limit=limit_a):
            if A.author.id == bot_id:
                await A.delete()
    else:
        #public channels
        if get_bot_perms(message).manage_messages == False:
            await message.reply('i dont have `manage messages` in here dummy', mention_author=True)
            return
        if message.author.guild_permissions.manage_messages == False:
            await message.reply('you dont have `manage messages` in here dummy', mention_author=True)
            return
        await message.channel.purge(limit=limit_a)

async def change_game(game):
    await client.change_presence(status=discord.Status.online, activity=discord.Game(game))

def unpack_keys(dict):
    return [*dict]

def get_bot_perms(message):
    #gets the channel obj, then gets the perms for the bot in the channel 
    return client.get_channel(message.channel.id).permissions_for(message.guild.me)

#TODO switch over again to json
def cmd_builder():
    #print(os.getcwd())
    with open("command_list.csv", "r") as workfile:
        command_list_reader = csv.DictReader(workfile,fieldnames=['name','desc','payload','trigger'],restkey='trigger')
        next(command_list_reader)
        for row in command_list_reader:
            t1 = command_no_promt_builder(cmd_name=row["name"],cmd_payload=row["payload"],cmd_desc=row["desc"],cmd_trigger=row['trigger'])
            cmd_list.append(t1)
        workfile.close()


client = MyClient()
def starttime():
    client.run(bot_token)


if __name__ == "__main__":
    starttime()