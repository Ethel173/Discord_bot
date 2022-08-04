#split for readability 
#handles chat events 
#
#
from no_command_response import reply_bot_message


def check_message_processor(self, message):
        #check if it was a 'no command' interaction
        return_struct = reply_bot_message(self, message)
        #returns false if nothing happened
        if return_struct != False:
            return return_struct
        return False
        #TODO add slash commands handler 