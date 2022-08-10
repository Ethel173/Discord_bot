import json
import re
import sys
from envflags import bot_id,owner_id
import discord
from project import roll_random_in_array,reload,psudo_list_rng

startup_statuses = []
startup_statuses  = []
scared_responses = []
un_scared_response = []
RNG_like_dislike = []
insults = []
cmd_list = []
admin_success = []
mod_client = ''
status_current = ''
reply_prefix = ''
flag_ping_user = False
flag_scare = False
#reloadable debug flag
#assignments are 'debug_default' or True / False
debug_mode = False


#reply_prefix builder
async def pre_message_builder_and_caller(message, command,regex = ''):
    global reply_prefix
    global flag_scare
    global flag_ping_user
    ###DEBUG RIP ME OUT FOR RELEASE
    if debug_mode == True:
        print('processing {0.author}: {0.content} '.format(message))
    #clear it for new response
    #handle yelling
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
    await eval(command +"(message, command, regex)")




#reloadable commands to search for
#TODO see if can rip regex = '' out 

#generic pong
async def hw(message, command, regex = ''):
    await message.reply(reply_prefix + 'hello there!', mention_author = flag_ping_user)

###owner command
async def game_roll(message, command, regex = ''):
        if message.author.id == owner_id:
            psudo_rng = psudo_list_rng(startup_statuses,status_current)
            psudo_change_game = roll_random_in_array(psudo_rng)
            await message.reply(reply_prefix + 'im trying ok', mention_author = flag_ping_user)
            await mod_client.change_presence(status=discord.Status.online, activity=discord.Game(psudo_change_game))

#purge chat event, calls the helper further down 
###needs both people to have `manage messages`
async def purge(message, command, regex = ''):
    purge_number = message.content.lower().replace(regex,'')
    try:
        limit_a = int(purge_number)
        if limit_a < 2 or limit_a > 100:
            raise TypeError
    except TypeError:
            await message.reply('thats not a good number ' + str(roll_random_in_array(insults))+ ' needs to be between 2 and 100', mention_author=True)
            return
    #DMS or private groups, bot had some perms by default
    if message.channel.type.value == 1:
        async for each_message in message.channel.history(limit=limit_a):
            if each_message.author.id == bot_id:
                await each_message.delete()
    else:
        #'public' channels
        if message.guild.me.permissions_in(message.channel).manage_messages == False:
            await message.reply('i dont have `manage messages` in here ' + str(roll_random_in_array(insults)), mention_author=True)
            return
        elif message.channel.permissions_for(message.author).manage_messages == False:
            await message.reply('you dont have `manage messages` in here ' + str(roll_random_in_array(insults)), mention_author=True)
            return
        else:
            try:
                yeetcounter = await message.channel.purge(limit=limit_a)
                await message.send('deyeeted {} message(s)'.format(len(yeetcounter)))
            except discord.HTTPException:
                await message.send('something happened with the network\n try again?')

#rng like dislike
async def rng_like(message, command, regex = ''):
    like_dislike = message.content.lower().replace(regex,' ')
    await message.reply(reply_prefix + roll_random_in_array(RNG_like_dislike) + like_dislike, mention_author=flag_ping_user)

#generic google search
async def search(message, command, regex = ''):
    search_tag = message.content.lower().replace(regex,' ')
    await message.reply(reply_prefix + 'https://www.google.com/search?q='+ search_tag.replace(' ','+'), mention_author=True)

#image search
async def source(message, command, regex = ''):
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
async def help(message, command, regex = ''):    
    if message.channel.type.value == 1:
        channel = message.channel
        for i in range(len(cmd_list)):
            if cmd_list[i]['hidden'] == 'False':
                megablock = 'command: '+ str(cmd_list[i]['name'])+'\n description: '+str(cmd_list[i]['description'])+'\n trigger words: '+str(cmd_list[i]['trigger'])+'\n ------\n'
                await channel.send(megablock)
        await channel.send('i think thats it')
        return
    else:
        await message.reply('ask again in dms ' + roll_random_in_array(insults) + '\nim not flooding chat', mention_author=True)

#reload command 
#does a wierd jump back into main file and somehow doesnt cause recursion
async def reload_everything(message, command, regex = ''):
    if message.author.id == owner_id:
        await reload(message)


###command builder
def personality_builder():
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