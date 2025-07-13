# twitch-discord-bot
some simple python scripts for a discord bot that alerts you when 1 or more streamers go live, offline, or change their stream title (even while offline).
should be pretty easy to remove features you don't like (eg: title change) by just deleting the relevant code.

 <br />

imports:
```python
discord.py
aiohttp
```

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
