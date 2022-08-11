import json
import re
from envflags import bot_id,owner_id
import discord
from project import roll_random_in_array,reload_commands,psudo_list_rng,debug_default,str_to_bool
startup_statuses = []
scared_responses = []
un_scared_response = []
RNG_like_dislike = []
insults = []
cmd_list = []
admin_success = []
status_current = ''
reply_prefix = ''
flag_ping_user = False
flag_scare = False
#reloadable debug flag
#assignments are 'debug_default' or True / False
debug_mode = debug_default
startup = False

#reply_prefix builder
async def pre_message_builder_and_caller(client, message, command, regex = ''):
    global reply_prefix
    global flag_scare
    global flag_ping_user
    ###DEBUG RIP ME OUT FOR RELEASE
    if debug_mode == True:
        print('processing {0.author}: {0.content} '.format(message))
    #handle yelling and clear it for new response
    if message.content.isupper():
        reply_prefix = roll_random_in_array(scared_responses) +' '
        flag_ping_user = True
        flag_scare = True
    elif flag_scare == True:
            reply_prefix = roll_random_in_array(un_scared_response) +' '
            ###DEBUG RIP ME OUT FOR RELEASE
            if debug_mode == True:
                print("trip thank flag")
            flag_scare = False
    else:
        reply_prefix = ''
    #fire subroutine with direct input args
    await eval(command +"(client, message, regex)")




#reloadable commands to search for

#generic pong
async def hw(client, message, extra_data = ''):
    await message.reply(reply_prefix + 'hello there!', mention_author = flag_ping_user)

#change game
###owner command
async def game_roll(client, message, extra_data = ''):
    if message.author.id != owner_id:
        return
    await set_new_game(client, extra_data)
    await message.reply(reply_prefix + roll_random_in_array(admin_success), mention_author = True)
#used on initalize
async def set_new_game(client, extra_data = ''):
    global status_current
    global startup
    if startup == False:
        status_current = roll_random_in_array(startup_statuses)
        startup = True
    elif extra_data == '':
        psudo_rng = psudo_list_rng(startup_statuses,status_current)
        status_current = roll_random_in_array(psudo_rng)
    else:
        status_current = extra_data
    await client.change_presence(status=discord.Status.online, activity=discord.Game(status_current))

#purge chat event, calls the helper further down 
###needs both people to have `manage messages`
async def purge(client, message, extra_data = ''):
    try:
        extra_data = int(extra_data)
        if extra_data < 2 or extra_data > 100:
            raise TypeError
    except TypeError:
            await message.reply('thats not a good number ' + str(roll_random_in_array(insults))+ ' needs to be between 2 and 100', mention_author=True)
            return
    #DMS or private groups, bot had some perms by default
    if message.channel.type.value == 1:
        yeetcounter = 0
        async for each_message in message.channel.history(limit=extra_data):
            if each_message.author.id == bot_id:
                yeetcounter += 1
                await each_message.delete()
        await message.channel.send(f'deyeeted {str(yeetcounter)} of my message(s)')
    else:
        #'public' channels
        if message.guild.me.permissions_in(message.channel).manage_messages == False:
            await message.reply('i dont have `manage messages` in here ' + str(roll_random_in_array(insults)), mention_author=True)
            return
        elif message.channel.permissions_for(message.author).manage_messages == False:
            await message.reply('you dont have `manage messages` in here ' + str(roll_random_in_array(insults)), mention_author=True)
            return
    #passed all checks go yeet
        yeetcounter = await message.channel.purge(limit=extra_data)
        await message.channel.send('deyeeted '+str(len(yeetcounter))+' message(s)')

#rng like dislike
async def rng_like(client, message, extra_data = ''):
    await message.reply(reply_prefix + roll_random_in_array(RNG_like_dislike) +' '+ extra_data, mention_author=flag_ping_user)

#generic google search
async def search(client, message, extra_data = ''):
    await message.reply(reply_prefix + 'https://www.google.com/search?q='+ extra_data.replace(' ','+'), mention_author=True)

#image search
async def source(client, message, extra_data = ''):
    if len(message.attachments) == 0:
        return
    results_list = reply_prefix
    for i in range(0,len(message.attachments)):
        pixiv = re.search('\d+(?=_p\d+\.?\_?)',str(message.attachments[i-1].url))
        if pixiv:
            hunt  = pixiv[0]
            results_list = results_list + 'i think this might be a pixiv image\n' + 'https://www.pixiv.net/en/artworks/'+str(hunt)+'\n'
        else:
            hunt = str(message.attachments[i-1].url).replace('http://','').replace('https://','')
            results_list = results_list + 'am dumm, so heres google\n' +'https://www.google.com/searchbyimage?image_url='+str(hunt)+'\n'
    await message.reply(results_list, mention_author=True)


###help
async def help(client, message, extra_data = ''):    
    #check if in public channels
    if message.channel.type.value != 1:
        #dont print out the message for a generic 'help' post
        if message.content.lower().startswith("help"):
            return
        await message.reply('ask again in dms ' + roll_random_in_array(insults) + '\nim not flooding chat', mention_author=True)
        return
    #we are in dms
    #buffer for chunking messages together
    block_counter = 0
    block_chunker = 3
    megablock = ''
    #return all
    for help_all in range(len(cmd_list)):
        if block_counter % block_chunker == 0:
            megablock = ''
        if cmd_list[help_all]['hidden'] == 'False':
            block_counter += 1
            megablock = megablock +'command: '+ str(cmd_list[help_all]['name'])+'\ndescription: '+str(cmd_list[help_all]['description'])+'\ntrigger words: '+str(cmd_list[help_all]['trigger'])+'\n ------\n'
        elif message.author.id == owner_id:
            block_counter += 1
            megablock = megablock +'ADMIN: '+ str(cmd_list[help_all]['name'])+'\ndescription: '+str(cmd_list[help_all]['description'])+'\ntrigger words: '+str(cmd_list[help_all]['trigger'])+'\n ------\n'

        if block_counter % block_chunker == 0:
            await message.channel.send("```"+ megablock+"```")
    
    #force send if there is a message in buffer
    if block_counter % block_chunker != 0:
        await message.channel.send("```"+ megablock+"```")
    await message.channel.send('i think thats it')
    return


#change debug flag
###owner command
async def c_db_flag(client, message, extra_data = ''):
    global debug_mode
    if message.author.id != owner_id:
        return
    tryme = extra_data.title().strip(' ')
    try_debug = str_to_bool(tryme)
    if try_debug != True and try_debug != False:
        await message.reply("invalid debug flag asisgnment :"+tryme, mention_author=True)
    else:
        debug_mode = try_debug
        await message.reply(roll_random_in_array(admin_success) +"\ndebug : "+str(debug_mode), mention_author=True)

#reload command 
#does a wierd jump back into main file and somehow doesnt cause recursion
async def reload_cmds(client, message, extra_data = ''):
    if message.author.id == owner_id:
        await reload_commands(message)





###command builder
def commands_data_loader():
    global startup_statuses
    global scared_responses
    global un_scared_response
    global RNG_like_dislike
    global insults
    global admin_success
    with open("command_list.json", "r") as workfile:
        command_list = json.load(workfile)
        startup_statuses = command_list['statuses']
        scared_responses = command_list['scared_responses']
        un_scared_response = command_list['un_scared_response']
        RNG_like_dislike = command_list['RNG_like_dislike']
        admin_success = command_list['admin_success']
        insults = command_list['insult']
        for i in range(len(command_list['commands'])):
            p1 = command_list['commands'][i]
            cmd_list.append(p1)
        workfile.close()