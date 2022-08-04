#handles any 'no command' chat events
#
#
import os
import dotenv 
#load env flags
dotenv.load_dotenv()
debug = bool(os.getenv('DEBUG'))
bot_token = os.getenv('DISCORD_TOKEN')

scare_flag = False
yell_at_user_flag = False

class bot_return_struct:
    def __init__(self, string, userflag):
        self.string = string
        self.userflag = userflag
    def rtr_resp(self):
        return self.string
    def rtr_flag(self):
        return self.userflag


#self is unused currently
def reply_bot_message(self, message):
    bot_reply = ''
    global scare_flag
    global yell_at_user_flag
    yell_at_user_flag = False
    action_flag = 0
    if debug == True:
        print('processing {0.author}: {0.content} '.format(message))

    #alis for cleaner reading
    #intake = original conent, (used later), lower for handling logic
    intake = message.content
    intake_lower = intake.lower()


    if intake_lower.startswith('hello'):
        bot_reply = bot_reply + 'Hello!'
        action_flag = 1

    proc1 = ''
    #make sure to add in the ' '
    search_keywords = ['googlefu ','can the internet tell me why ' ]
    for i in search_keywords:
        #check if this loop works properly
        if debug == True:
            print('checking for ',i)
        if intake_lower.startswith(str(i)):
            proc1 = intake_lower.replace(str(i),'')
            bot_reply = bot_reply + 'https://www.google.com/search?q='+str(proc1).replace(' ','+')
            action_flag = 1
            break

    #failsale flag to return custom message, not needed but nice 
    if action_flag == 1:

        #'yelling' flavor text
        #in here to only process scare flags if responding to comething
        #uses intake as alias for original message
        if intake.isupper():
            bot_reply = 'Please stop yelling at me its scawwy but ' + bot_reply
            yell_at_user_flag = True
            scare_flag = True
        else:
            if scare_flag == True:
                    bot_reply = 'Thankies and ' + bot_reply
                    if debug == True:
                        print("trip thank flag")
                    scare_flag = False
        if debug == True:
            print("tried sending message: -" + str(bot_reply) + '- with UT_flag: -' + str(yell_at_user_flag) +'-')
        return bot_return_struct(bot_reply, yell_at_user_flag)
    #failsafe return false
    return False