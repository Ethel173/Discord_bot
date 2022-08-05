#workaround for circular import errors

import os
import sys
import dotenv 

#load env flags
dotenv.load_dotenv()
client_id = os.getenv('CLIENT_ID')
guild_id = os.getenv('GUILD_ID')
bot_token = os.getenv('DISCORD_TOKEN')
debug = os.getenv('DEBUG')
home_channel = os.getenv('HOME_CHANNEL')

try:
    if home_channel == '':
        home_channel = False
    else:
        home_channel = int(home_channel)
except TypeError:
    sys.exit("invalid HOME_CHANNEL assignment")



if __name__ == "__main__":
    sys.exit(1)