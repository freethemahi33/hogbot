import discord
import responses
from discord.ext import commands
import youtube_dl


class MusicBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None
        print("Music bot has been initialized.")

    # Join the voice channel
    @commands.command()
    async def join(self, ctx):
        print("Join command received")
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"I have joined the voice channel {channel.name}!")

    # Leave the voice channel
    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    # Play music from YouTube
    @commands.command()
    async def play(self, ctx, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            ctx.voice_client.stop()
            ctx.voice_client.play(discord.FFmpegPCMAudio(url2))

    # Stop playing music
    @commands.command()
    async def stop(self, ctx):
        ctx.voice_client.stop()


def remove_bot_mention(content, bot_id):
    mention_formats = [
        f"<@{bot_id}>",
        f"<@!{bot_id}>"
    ]
    for mention_format in mention_formats:
        content = content.replace(mention_format, '').strip()
    return content


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message, message.author.display_name)
        print(f"Response from handle_response: {response}")  # Debug line
        if response:
            if is_private:
                print("Sending private message")  # Debug line
                await message.author.send(response)
            else:
                print("Sending public message")  # Debug line
                await message.channel.send(response)
    except Exception as e:
        print(e)


# Set up the bot
client = commands.Bot(command_prefix='!', intents=discord.Intents.default())


@client.command()
async def playsong(ctx, artist, song_name):
    # Search YouTube for the artist and song name
    query = f"{artist} {song_name}"
    with youtube_dl.YoutubeDL() as ydl:
        search_results = ydl.extract_info(f"ytsearch:{query}", download=False)
        if not search_results["entries"]:
            await ctx.send("No search results found.")
            return
        url = search_results["entries"][0]["webpage_url"]

    # Play the audio from the URL
    voice_client = ctx.voice_client
    voice_client.stop()
    voice_client.play(discord.FFmpegPCMAudio(url))


@client.event
async def on_ready():
    print(f'{client.user} is now running')


@client.event
async def on_message(message):
    print(f"Message received from {message.author}: {message.content}")
    if message.author == client.user:
        return

    if message.content.startswith('!join'):
        print("call join")
        await MusicBot.join(MusicBot(client), message)

    if client.user.mentioned_in(message):
        user_message = remove_bot_mention(message.content, client.user.id)
        print(f"User message after removing mention: {user_message}")
        is_private = isinstance(message.channel, discord.abc.PrivateChannel)
        await send_message(message, user_message, is_private)

    await client.process_commands(message)



def run_discord_bot():
    TOKEN = ''
    intents = discord.Intents.default()
    intents.messages = True
    intents.guilds = True
    intents.voice_states = True

    music_bot = MusicBot(client)
    client.add_cog(music_bot)
    client.run(TOKEN)


run_discord_bot()
