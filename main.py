import json
from fileinput import close
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
startup_statuses = []
startup_status_current = ''
scared_responses = []
un_scared_response = []
RNG_like_dislike = []

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
        global startup_status_current
        print('Logged in as = ' +str(self.user.name))
        print('with userid = ' + str(bot_id))
        print('------')
        await cmd_builder()
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
        if message.channel.type.value != 1:
            if get_channel_perms(message, message.guild.me).send_messages == False:
                return
        #debug
        if debug == True:
            print('caught message: {0.author}: {0.content}'.format(message))

    #start logic
    #chat events that return a response
        for cmd in range(len(cmd_list)):
            p2 = False
            if type(cmd_list[cmd]['trigger']) != list:
                if re.match(cmd_list[cmd]['trigger'],message.content.lower()):
                    p2 = await reply_bot_message(message, cmd_list[cmd]['payload'])
            else:
                for i in range(0,len(cmd_list[cmd]['trigger'])):
                    if re.match(cmd_list[cmd]['trigger'][i],message.content.lower()):
                        p2 = await reply_bot_message(message, cmd_list[cmd]['payload'],cmd_list[cmd]['trigger'][i])
            if p2 != False: 
                if p2.rtr_resp()!="":
                    await message.reply(p2.rtr_resp(), mention_author=p2.rtr_flag())

    async def on_message_delete(self,message):
        if message.author.id == bot_id:
            return
            #dont fire in DMs
        elif message.channel.type.value != 1:
            channel = client.get_channel(message.channel.id)
            await channel.send("i saw that")


#message handler
async def reply_bot_message(message, command,regex = ''):
    global bot_reply
    global flag_scare
    global flag_ping_user
    if debug == True:
        print('processing {0.author}: {0.content} '.format(message))
    #clear it for new response
    bot_reply = ''
    async def game_roll(message):
        global bot_reply
        bot_reply = "im trying ok"
        psudo_rng = psudo_list_rng(startup_statuses,startup_status_current)
        psudo_change_game = roll_random_in_array(psudo_rng)
        await change_game(psudo_change_game)
    async def hw(message):
        global bot_reply
        bot_reply = 'Hello!'
    async def purge(message):
        proc1 = message.content.lower().replace(command+' ','')
        await mass_del(message,proc1)
        channel = client.get_channel(message.channel.id)
        return False
    async def rng_like(message):
        global bot_reply
        proc1 = message.content.lower().replace('hey gura what do you think of ','')
        bot_reply = roll_random_in_array(RNG_like_dislike) + proc1
    async def search(message):
        global bot_reply
        proc1 = message.content.lower().replace(regex,'')
        bot_reply = 'https://www.google.com/search?q='+proc1.replace(' ','+')    
    async def source(message):
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
    async def reload(message):
        global bot_reply
        await cmd_builder()
        bot_reply = 'done'
    async def help(message):    
        if message.channel.type.value == 1:
            channel = client.get_channel(message.channel.id)
            for i in range(len(cmd_list)):
                megablock = ''
                megablock = megablock +'command: '+ str(cmd_list[i]['name'])+'\n description: '+str(cmd_list[i]['description'])+'\n trigger words: '+str(cmd_list[i]['trigger'])+'\n ------\n'
                await channel.send(megablock)
            await channel.send('i think thats it')
            return False
        else:
            await message.reply('ask again in dms ' + str(roll_random_in_array(insults)) + ' im not flooding chat', mention_author=True)



    #fire subroutine
    await eval(command+"(message)")
    #handle yelling
    if message.content.isupper():
        bot_reply = roll_random_in_array(scared_responses) + bot_reply
        flag_ping_user = True
        flag_scare = True
    else:
        if flag_scare == True:
                bot_reply = roll_random_in_array(un_scared_response) + bot_reply
                if debug == True:
                    print("trip thank flag")
                flag_scare = False
    if debug == True:
        print("tried sending message: -" + str(bot_reply) + '- with yell_flag: -' + str(flag_ping_user) +'-')
    return bot_return_struct(bot_reply, flag_ping_user)

async def mass_del(message,number):
    try:
        limit_a = int(number)
        if limit_a <= 1:
            raise TypeError
    except TypeError:
            await message.reply('thats not a good number ' + str(roll_random_in_array(insults)),+ ' needs to be 2 or bigger', mention_author=1)
            return False
    #DMS or private groups
    if message.channel.type.value == 1:
        async for A in message.channel.history(limit=limit_a):
            if A.author.id == bot_id:
                await A.delete()
    else:
        #public channels
        #alpha = message.channel.permissions_for(message.guild.me)
        if message.guild.me.permissions_in(message.channel).manage_messages == False:
            await message.reply('i dont have `manage messages` in here ' + str(roll_random_in_array(insults)), mention_author=True)
            return False
        elif message.channel.permissions_for(message.author).manage_messages == False:
        #if get_channel_perms(message, message.author).manage_messages == False:
            await message.reply('you dont have `manage messages` in here ' + str(roll_random_in_array(insults)), mention_author=True)
            return False
        else:
            await message.channel.purge(limit=limit_a)
            await message.channel.send('deyeeted up to '+str(limit_a)+' messages \nidk im not counting')

async def change_game(game):
    await client.change_presence(status=discord.Status.online, activity=discord.Game(game))

def unpack_keys(dict):
    return [*dict]

def get_channel_perms(message,user):
    #gets the channel obj, then gets the perms for the bot in the channel 
    return client.get_channel(message.channel.id).permissions_for(user)


async def cmd_builder():
    global cmd_list
    global startup_statuses
    global scared_responses
    global un_scared_response
    global RNG_like_dislike
    global insults
    with open("gamer_list.json", "r") as workfile:
        command_list = json.load(workfile)
        startup_statuses = command_list['statuses']
        scared_responses = command_list['scared_responses']
        un_scared_response = command_list['un_scared_response']
        RNG_like_dislike = command_list['RNG_like_dislike']
        insults = command_list['insult']
        for i in range(len(command_list['commands'])):
            p1 = command_list['commands'][i]
            cmd_list.append(p1)
        workfile.close()

client = MyClient()
def starttime():
    client.run(bot_token)


if __name__ == "__main__":
    starttime()