import importlib
import random
import re
import sys
import discord
from envflags import bot_id,bot_token,debug,home_channel
import sys

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
flag_scare = False
flag_ping_user = False
no_dupe_logins = True
current_status = ''

#helper funcs
def unpack_keys(dict):
    return [*dict]

def roll_random_in_array(rng_array,seed_val=0):
    if seed_val != 0:
        random.seed(seed_val)
    #need -1 since index starts at 0 but len starts at 1
    i = random.randint(0,len(rng_array)-1)
    return rng_array[i]

def psudo_list_rng(list_a,str_t):
    res = [i for i in list_a if str_t not in i]
    return res

##janky hack to prevent circular imports in pytest
if "pytest" not in sys.modules:
    import commands

    class MyClient(discord.Client):
        global current_status
        async def on_ready(self):
            print('Logged in as = ' +str(self.user.name))
            print('with userid = ' + str(bot_id))
            print('------')
            startup_status_current = roll_random_in_array(commands.startup_statuses)
            await client.change_presence(status=discord.Status.online, activity=discord.Game(startup_status_current))
            if home_channel != False:
                ###DEBUG RIP ME OUT FOR RELEASE
                if commands.debug_mode == True:
                    print('tried mentioning startup in channel :', client.get_channel(home_channel))
                await client.get_channel(home_channel).send("bot online")
            #needed to populate commands imported arrays
            commands.status_current = startup_status_current
            commands.mod_client = client

        async def on_message(self, message):
            #prevent replies and logging of bot messages
            if message.author.id == bot_id:
                ###DEBUG RIP ME OUT FOR RELEASE
                if commands.debug_mode == True:
                    print('discarded self-message: {0.author}: {0.content}'.format(message))
                return

            #abort if cant send messages in channel
            if message.channel.type.value != 1:
                if message.channel.permissions_for(message.author).send_messages == False:
                    return
                ###DEBUG RIP ME OUT FOR RELEASE
                if commands.debug_mode == True:
                    print('caught message: {0.author}: {0.content}'.format(message))

            #chat command event seeker
            for command_index in range(len(commands.cmd_list)):
                if type(commands.cmd_list[command_index]['trigger']) != list:
                    if re.match(commands.cmd_list[command_index]['trigger'],message.content.lower()):
                        #pass current status
                        #TODO find a better way to do this instead of every command
                        commands.status_current = current_status
                        await commands.pre_message_builder_and_caller(message, commands.cmd_list[command_index]['payload'],commands.cmd_list[command_index]['trigger'])
                else:
                    for trigger_index in range(0,len(commands.cmd_list[command_index]['trigger'])):
                        if re.match(commands.cmd_list[command_index]['trigger'][trigger_index],message.content.lower()):
                            #TODO same here
                            commands.status_current = current_status
                            await commands.pre_message_builder_and_caller(message, commands.cmd_list[command_index]['payload'],commands.cmd_list[command_index]['trigger'][trigger_index])

        async def on_message_delete(self,message):
            if message.author.id == bot_id:
                return
                #dont fire in DMs
            elif message.channel.type.value != 1:
                channel = client.get_channel(message.channel.id)
                await channel.send("i saw that")

    ###reload function
    async def reload(message):
        #reload the file
        importlib.reload(commands)
        #load things from json
        commands.personality_builder()
        #reset the current status since its null
        commands.status_current = current_status
        #reset the client obj status since its null
        commands.mod_client = client
        await message.reply(roll_random_in_array(commands.admin_success))

    #initial set command file variables
    def populate_commands():
        commands.personality_builder()


    client = MyClient()
    def starttime():
        global no_dupe_logins
        if no_dupe_logins == True:
            no_dupe_logins = False
            populate_commands()
            client.run(bot_token)
        else:
            print('ERROR PREVENTED\n---\nsupressed a duplicate login attempt')


    if __name__ == "__main__":
        starttime()