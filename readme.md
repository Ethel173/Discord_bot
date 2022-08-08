# Discord Chat Bot
#### Video Demo:  <URL HERE>
#### Description:
uses discord.py,
uses a needlessly complicated loop to parse regex patterns to call commands since i could not for the life of me get /interactions to work with any library

a summary of the commands, which can also be called in DM channels using triggers for `help` :
```
command: hello
description: replies back hello
trigger words: hello

command: google search
description: standard google search,search
trigger words: ['googlefu ', 'can the internet tell me why ', 'explain to me ']

command: RNG like dislike
description: replies back if bot likes or dislikes message content
trigger words: hey gura what do you think of 

command: reverse image search
description: replies back with a pixiv or google search for every attached image
trigger words: source me

command: purge messages
description: blindly deletes X messages (if it can), as long as the message is < 14 days old
trigger words: purge 

command: change game
description: change game displayed on bot profile
trigger words: gura change your game

command: reload commands
description: reload commands
trigger words: gura reload

command: help
description: sends all loaded commands
trigger words: gura help
```

the trigger word(s)/phrase(s) for commands and any personality flair are dynamically loaded from command_list.json and can be refreshed while the bot is online with the `reload commands` func, though any new functions will require a restart

dotenv arguments are handled in an intermediate envflags.py file

utils.py hold some minor code snippets that might be useful outside the bot

the bot doesnt like it when you yell at it