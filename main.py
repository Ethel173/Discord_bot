import importlib
import json
import re
import sys
import discord
from envflags import bot_id,bot_token,debug,home_channel,owner_id
from utils import roll_random_in_array,psudo_list_rng
import commands
#has to be up here for debug assignment
#pythons built in bool(X) doesnt convert 'False' into False
def str_to_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        sys.exit("invalid debug asisgnment in .env")
debug_default = str_to_bool(debug)
#globals
bot_reply = ''
flag_scare = False
flag_ping_user = False
no_dupe_logins = True
#flavor text


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as = ' +str(self.user.name))
        print('with userid = ' + str(bot_id))
        print('------')
        await populate_commands()
        startup_status_current = roll_random_in_array(commands.startup_statuses)
        await change_game(startup_status_current)
        if home_channel != False:
            #channel = client.get_channel(home_channel)
            if commands.debug_mode == True:
                print('tried mentioning startup in channel :', client.get_channel(home_channel))
            await client.get_channel(home_channel).send("bot online")
        #needed to populate commands imported arrays
        commands.startup_status_current = startup_status_current

    async def on_message(self, message):
        #prevent replies and logging of bot messages
        if message.author.id == bot_id:
            if commands.debug_mode == True:
                print('discarded self-message: {0.author}: {0.content}'.format(message))
            return
        #abort if cant send messages
        if message.channel.type.value != 1:
            if get_channel_perms(message, message.guild.me).send_messages == False:
                return
        #debug
        if commands.debug_mode == True:
            print('caught message: {0.author}: {0.content}'.format(message))

        #chat command event handler
        for command_index in range(len(commands.cmd_list)):
            if type(commands.cmd_list[command_index]['trigger']) != list:
                if re.match(commands.cmd_list[command_index]['trigger'],message.content.lower()):
                    await pre_message_builder_and_caller(message, commands.cmd_list[command_index]['payload'],commands.cmd_list[command_index]['trigger'])
            else:
                for trigger_index in range(0,len(commands.cmd_list[command_index]['trigger'])):
                    if re.match(commands.cmd_list[command_index]['trigger'][trigger_index],message.content.lower()):
                        await pre_message_builder_and_caller(message, commands.cmd_list[command_index]['payload'],commands.cmd_list[command_index]['trigger'][trigger_index])
                        
    async def on_message_delete(self,message):
        if message.author.id == bot_id:
            return
            #dont fire in DMs
        elif message.channel.type.value != 1:
            channel = client.get_channel(message.channel.id)
            await channel.send("i saw that")


#message builder
async def pre_message_builder_and_caller(message, command,regex = ''):
    global bot_reply
    global flag_scare
    global flag_ping_user
    if commands.debug_mode == True:
        print('processing {0.author}: {0.content} '.format(message))
    #clear it for new response
    #handle yelling
    if message.content.isupper():
        bot_reply = roll_random_in_array(commands.scared_responses) +' '
        flag_ping_user = True
        flag_scare = True
    elif flag_scare == True:
            bot_reply = roll_random_in_array(commands.un_scared_response) +' '
            if commands.debug_mode == True:
                print("trip thank flag")
            flag_scare = False
    else:
        bot_reply = ''
    #fire subroutine with direct input args
    await eval('commands.'+ command +"(message, command, regex,bot_reply,flag_ping_user)")


###reload function
async def reload(message):
    importlib.reload(commands)
    commands.personality_builder()
    await message.reply(bot_reply + 'locked and loaded')
#set vars for commands
async def populate_commands():
    commands.personality_builder()


###helpers
async def change_game(game):
    await client.change_presence(status=discord.Status.online, activity=discord.Game(game))


async def main_help(message):
    if message.channel.type.value == 1:
        channel = message.channel
        for i in range(len(commands.cmd_list)):
            if commands.cmd_list[i]['hidden'] == 'False':
                megablock = 'command: '+ str(commands.cmd_list[i]['name'])+'\n description: '+str(commands.cmd_list[i]['description'])+'\n trigger words: '+str(commands.cmd_list[i]['trigger'])+'\n ------\n'
                await channel.send(megablock)
        await channel.send('i think thats it')
        return
    else:
        await message.reply('ask again in dms ' + roll_random_in_array(commands.insults) + ' im not flooding chat', mention_author=True)


def unpack_keys(dict):
    return [*dict]

def get_channel_perms(message,user):
    #gets the channel obj, then gets the perms for the bot in the channel 
    return client.get_channel(message.channel.id).permissions_for(user)

client = MyClient()
def starttime():
    global no_dupe_logins
    if no_dupe_logins == True:
        no_dupe_logins = False
        client.run(bot_token)
    else:
        print('ERROR PREVENTED\n---\nsupressed a duplicate login attempt')

if __name__ == "__main__":
    starttime()