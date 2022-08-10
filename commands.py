import json
import re
from main import bot_reply,change_game,psudo_list_rng,flag_ping_user
from main import roll_random_in_array,reload,debug_default,main_help
from envflags import bot_id,owner_id

startup_statuses = []
startup_statuses  = []
scared_responses = []
un_scared_response = []
RNG_like_dislike = []
insults = []
startup_status_current = ''
cmd_list = []


#reloadable debug flag
#assignments are 'debug_default' or True / False
debug_mode = False

#reloadable commands to search for
###owner command
async def game_roll(message, command, regex = '',bot_reply = '',flag_ping = False):
        if message.author.id == owner_id:
            psudo_rng = psudo_list_rng(startup_statuses,startup_status_current)
            psudo_change_game = roll_random_in_array(psudo_rng)
            await change_game(psudo_change_game)
            await message.reply(bot_reply + 'im trying ok', mention_author = flag_ping)

async def hw(message, command, regex = '',bot_reply = '',flag_ping = False):
    await message.reply(bot_reply + 'hello there!', mention_author = flag_ping)

async def purge(message, command, regex = '',bot_reply = '',flag_ping = False):
    purge_number = message.content.lower().replace(regex,'')
    await mass_del(message,purge_number)

async def rng_like(message, command, regex = '',bot_reply = '',flag_ping = False):
    like_dislike = message.content.lower().replace(regex,' ')
    await message.reply(bot_reply + roll_random_in_array(RNG_like_dislike) + like_dislike, mention_author=flag_ping)

async def search(message, command, regex = '',bot_reply = '',flag_ping = False):
    force_ping = True
    search_tag = message.content.lower().replace(regex,' ')
    await message.reply(bot_reply + 'https://www.google.com/search?q='+ search_tag.replace(' ','+'), mention_author=force_ping)

async def source(message, command, regex = '',bot_reply = '',flag_ping = False):
    if len(message.attachments) == 0:
        return
    for i in range(0,len(message.attachments)):
        pixiv = re.search('\d+(?=_p\d+\.?\_?)',str(message.attachments[i-1].url))
        if pixiv:
            hunt  = pixiv[0]
            bot_reply = bot_reply + 'i think this might be a pixiv image\n' + 'https://www.pixiv.net/en/artworks/'+str(hunt)+'\n'
        else:
            hunt = str(message.attachments[i-1].url).replace('http://','').replace('https://','')
            bot_reply = bot_reply + 'am dumm, so heres google\n' +'https://www.google.com/searchbyimage?image_url='+str(hunt)+'\n'
    await message.reply(bot_reply, mention_author=True)


async def reload_everything(message, command, regex = '',bot_reply = '',flag_ping = False):
    #do not touch me
    if message.author.id == owner_id:
        await reload(message)

###helpers
#needs both people to have `manage messages``
async def mass_del(message,number):
    try:
        limit_a = int(number)
        if limit_a <= 1:
            raise TypeError
    except TypeError:
            await message.reply('thats not a good number ' + roll_random_in_array(insults),+ ' needs to be 2 or bigger', mention_author=1)
            return
    #DMS or private groups
    if message.channel.type.value == 1:
        async for each_message in message.channel.history(limit=limit_a):
            if each_message.author.id == bot_id:
                await each_message.delete()
    else:
        #public channels
        if message.guild.me.permissions_in(message.channel).manage_messages == False:
            await message.reply('i dont have `manage messages` in here ' + roll_random_in_array(insults), mention_author=True)
            return
        elif message.channel.permissions_for(message.author).manage_messages == False:
            await message.reply('you dont have `manage messages` in here ' + roll_random_in_array(insults), mention_author=True)
            return
        else:
            await message.channel.purge(limit=limit_a)
            await message.channel.send('deyeeted up to '+str(limit_a)+' messages \nidk im not counting')


async def help(message, command, regex = '',bot_reply = '',flag_ping = False):    
    await main_help(message)


    ###command builder
def personality_builder():
    global startup_statuses
    global scared_responses
    global un_scared_response
    global RNG_like_dislike
    global insults
    with open("command_list.json", "r") as workfile:
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