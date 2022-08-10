#workaround for circular import errors

import os
import sys
import dotenv 

#load env flags
dotenv.load_dotenv()
bot_token = os.getenv('DISCORD_TOKEN')
if bot_token == False or bot_token == '':
    sys.exit("invalid DISCORD_TOKEN assignment")

try:
    home_channel = os.getenv('HOME_CHANNEL')
    if home_channel == '' or home_channel == 'False':
        home_channel = False
    else:
        home_channel = int(home_channel)
except:
    sys.exit("invalid HOME_CHANNEL assignment")

try:
    debug = os.getenv('DEBUG')
except:
    sys.exit("invalid DEBUG assignment")

try:
    bot_id = int(os.getenv('CLIENT_ID'))
except:
    sys.exit("invalid CLIENT_ID assignment")

try:
    guild_id = int(os.getenv('GUILD_ID'))
except:
    sys.exit("invalid GUILD_ID assignment")

try:
    home_guild = int(os.getenv('HOME_GUILD'))
except:
    sys.exit("invalid HOME_GUILD assignment")

try:
    owner_id = int(os.getenv('OWNER_ID'))
except:
    sys.exit("invalid OWNER_ID assignment")


if __name__ == "__main__":
    sys.exit(1)