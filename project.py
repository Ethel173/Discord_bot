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
debug_default = str_to_bool(debug)
#globals

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
        async def on_ready(self):
            print('Logged in as = ' +str(self.user.name))
            print('with userid = ' + str(bot_id))
            print('------')
            await commands.set_new_game(client)
            if home_channel != False:
                ###DEBUG RIP ME OUT FOR RELEASE
                if commands.debug_mode == True:
                    print('tried mentioning startup in channel :', client.get_channel(home_channel))
                await client.get_channel(home_channel).send("bot online")

        async def on_message(self, message):
            #prevent replies and logging of bot messages
            if message.author.id == bot_id:
                ###DEBUG RIP ME OUT FOR RELEASE
                if commands.debug_mode == True:
                    print('discarded self-message: {0.author}: {0.content}'.format(message))
                return

            #abort if cant send messages in channel
            if message.channel.type.value != 1:
                if message.channel.permissions_for(message.author).send_messages == None:
                    return
                ###DEBUG RIP ME OUT FOR RELEASE
                if commands.debug_mode == True:
                    print('caught message: {0.author}: {0.content}'.format(message))

            #chat command event seeker
            for command_index in range(len(commands.cmd_list)):
                if type(commands.cmd_list[command_index]['trigger']) != list:
                    ###DEBUG RIP ME OUT FOR RELEASE
                    if commands.debug_mode == True:
                        print("trying to match: "+commands.cmd_list[command_index]['trigger'])
                    if re.match(commands.cmd_list[command_index]['trigger'],message.content.lower()):
                        extra_data = message.content.lower().replace(commands.cmd_list[command_index]['trigger'],'')
                        await commands.pre_message_builder_and_caller(client, message, commands.cmd_list[command_index]['payload'],extra_data)
                else:
                    for trigger_index in range(0,len(commands.cmd_list[command_index]['trigger'])):
                        ###DEBUG RIP ME OUT FOR RELEASE
                        if commands.debug_mode == True:
                            print("trying to match: "+commands.cmd_list[command_index]['trigger'][trigger_index])
                        if re.match(commands.cmd_list[command_index]['trigger'][trigger_index],message.content.lower()):
                            extra_data = message.content.lower().replace(str(commands.cmd_list[command_index]['trigger'][trigger_index]),'')
                            await commands.pre_message_builder_and_caller(client, message, commands.cmd_list[command_index]['payload'],extra_data)

        async def on_message_delete(self,message):
            if message.author.id == bot_id:
                return
                #dont fire in DMs
            elif message.channel.type.value != 1:
                channel = client.get_channel(message.channel.id)
                await channel.send("i saw that")

    ###reload function
    async def reload_commands(message):
        #reload the file
        importlib.reload(commands)
        #populate the variables
        commands.commands_data_loader()
        await message.reply(roll_random_in_array(commands.admin_success))

    client = MyClient()
    def starttime():
        #initial set command file variables
        commands.commands_data_loader()
        client.run(bot_token)


    if __name__ == "__main__":
        starttime()