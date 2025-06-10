import discord
import asyncio
import json
from twitch import TwitchAPI

with open("config.json") as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
client = discord.Client(intents=intents)

twitch = TwitchAPI(config["twitch_client_id"], config["twitch_client_secret"])
STATE_FILE = "state.json"

def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

async def check_streams(channel):
    await twitch.authenticate()
    state = load_state()

    while True:
        live_data = await twitch.get_stream_data(config["streamers"])
        current_streams = {s["user_login"]: s for s in live_data}

        for name in config["streamers"]:
            live = current_streams.get(name)
            prev = state.get(name, {"live": False, "title": ""})

            # Handle going online
            if live and not prev["live"]:
                await channel.send(
                    f"🔴 **@everyone {name} is live!**\n"
                    f"**Title:** {live['title']}\n"
                    f"https://twitch.tv/{name}"
                )

            # Handle title change while live
            elif live and live["title"] != prev["title"]:
                await channel.send(
                    f"✏️ **@everyone {name} changed their title!**\n"
                    f"**New Title:** {live['title']}"
                )

            # Handle going offline
            elif not live and prev["live"]:
                await channel.send(f"⚫ **@everyone {name} went offline.**")

            # Detect title changes while offline
            if not live:
                # Store the last known title separately
                prev_title = prev.get("title", "")
                # Only update if the title changed
                if prev_title and prev_title != live["title"]:
                    await channel.send(
                        f"📃 **@everyone {name} changed their title!**\n"
                        f"**New Title:** {live['title']}"
                    )

            # Save the updated state
            state[name] = {
                "live": bool(live),
                "title": live["title"] if live else prev.get("title", "")
            }

        save_state(state)
        # this can almost certainly be shorter than 15 seconds. depends on how many streamers you're monitoring, I think? 1 second is honestly probably fine'
        await asyncio.sleep(15)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print("Connected servers:")
    for guild in client.guilds:
        print(f"- {guild.name} (ID: {guild.id})")
        for ch in guild.text_channels:
            print(f"  - #{ch.name} (ID: {ch.id})")

    channel = client.get_channel(int(config["channel_id"]))
    print(f"Channel resolved: {channel}")

    if channel is None:
        print("❌ Channel not found. Double-check the channel ID and bot's permissions.")
        return

    asyncio.create_task(check_streams(channel))

client.run(config["discord_token"])
