# twitch-discord-bot
some simple python scripts for a discord bot that alerts you when 1 or more streamers go live, offline, or change their stream title (even while offline).
should be pretty easy to remove features you don't like (eg: title change) by just deleting the relevant code.

 <br />

requires these packages (at least on fedora linux):

discord.py

aiohttp

 <br/>

run simply with `python bot.py`

for it to work you need to create a discord bot (application) and a twitch bot.

https://discord.com/developers/applications

https://dev.twitch.tv/console/apps

config.json requires:
- the token for your discord bot
- the channel ID of the channel in your sever that you want the bot to post to
- the twitch bot's client id
- the twitch bot's client secret
- the usernames of the streamers you wish to monitor.

line 78 of bot.py has the "ping" interval at 15 seconds, which is probably way too long
```python
# this can almost certainly be shorter than 15 seconds. depends on how many streamers you're monitoring, I think? 1 second is honestly probably fine'
        await asyncio.sleep(15)
```
