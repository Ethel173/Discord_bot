# Discord Chat Bot

uses discord.py,
uses a needlessly complicated loop to parse regex patterns to call commands since i could not for the life of me get /interactions to work with any library i tried

a summary of the commands, which can also be called in DM channels using triggers for `help` :
```
command: hello
 description: replies back hello
 trigger words: hello
 ------
command: google search
 description: standard google search,search
 trigger words: ['googlefu ', 'can the internet tell me why ', 'explain to me ']
 ------
command: RNG like dislike
 description: replies back if bot likes or dislikes message content
 trigger words: ['hey gura what do you think of ', 'gura what do you think of ', 'gura do you like ', 'gura do you hate ']
 ------
command: reverse image search
 description: replies back with a pixiv or google search for every attached image
 trigger words: source me
 ------
command: purge messages
 description: blindly deletes X messages (if it can), you need `manage messages`perms
bot cannot delete your message in DMs
 trigger words: purge 
 ------
command: help
 description: sends all loaded commands
 trigger words: gura help
 ------
```

the trigger word(s)/phrase(s) for commands and any personality flair are loaded from command_list.json and can be refreshed while the bot is online with the `reload commands`

dotenv arguments are handled in an intermediate envflags.py file for error checking

devbranch uses a janky workaround to prevent circular imports using pytest while still being able to test its functions

the bot doesnt like it when you yell at it,

please dont do that