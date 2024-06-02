import discord
import yt_dlp
import asyncio
from typing import List, Optional

from discord.ext import commands
from discord import Intents
from discord.ext.commands import Context

from config import Config

config = Config()

__TOKEN__ = config.TOKEN

tasker: Optional[asyncio.Task] = None

intents: Intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config.command_prefix, intents=intents)

DOWNLOAD_DIR = config.tracks_dir

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5) -> None:
        super().__init__(source, volume)
        self.data = data
        self.title: str = data.get('title')
        self.duration: float = data.get('duration')
        self.url: str = ""

    @classmethod
    async def from_url(cls, url: str, *, loop: Optional[asyncio.AbstractEventLoop] = None, stream: bool = False) -> 'YTDLSource':
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(f"ytsearch:{url}", download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


song_queue: List[YTDLSource] = []


@bot.command(name='leave', aliases=['l', 'exit'], help='To make the bot leave the voice channel')
async def leave(ctx: Context) -> None:
    voice_client = ctx.message.guild.voice_client
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        print("Disconnected from voice channel.")
    else:
        await ctx.send("The bot is not connected to a voice channel.")
        print("Tried to leave but was not connected to a voice channel.")


@bot.command(name='play', aliases=['p', 'play_song'], help='To play song')
async def play(ctx: Context, *, url: str) -> None:
    global song_queue
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        if voice is None:
            if not ctx.message.author.voice:
                await ctx.send(f"{ctx.message.author.name} is not connected to a voice channel")
                print(
                    f"{ctx.message.author.name} is not connected to a voice channel.")
            else:
                channel = ctx.message.author.voice.channel
                await channel.connect()
                print(f"Connected to voice channel: {channel}")
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=bot.loop, stream=False)
            song_queue.append(player)
            if not ctx.voice_client.is_playing():
                await start_playing(ctx)
            else:
                await ctx.send(f"**Queued at position {len(song_queue)}:** {player.title}")
                print(f"Queued song: {player.title}")

    except Exception as e:
        await ctx.send(f"Error occurred: {e}")
        print(f"Error occurred: {e}")


async def start_playing(ctx: Context) -> None:
    global song_queue
    while song_queue:
        current_song = song_queue.pop(0)
        ctx.voice_client.play(current_song, after=lambda e: (
            print(f'Player error: {e}') if e else bot.loop.create_task(start_playing(ctx))))
        await ctx.send(f"**Now playing:** {current_song.title}")
        print(f"Now playing: {current_song.title}")

        await asyncio.sleep(current_song.duration)
        print(f"Finished playing: {current_song.title}")


@bot.command(name='queued', aliases=['q', 'list'], help='This command displays the queue')
async def queued(ctx: Context) -> None:
    global song_queue
    a = ""
    for i, f in enumerate(song_queue):
        if i > 0:
            a += f"{i}. {f.title}\n"
    await ctx.send("Queued songs: \n" + a)
    print(f"Queued songs: \n{a}")


@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx: Context) -> None:
    voice_client = ctx.message.guild.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await ctx.send("Paused playing.")
        print("Paused playing.")
    else:
        await ctx.send("The bot is not playing anything at the moment.")
        print("Tried to pause but no song is playing.")


@bot.command(name='resume', help='Resumes the song')
async def resume(ctx: Context) -> None:
    voice_client = ctx.message.guild.voice_client
    if voice_client and voice_client.is_paused():
        voice_client.resume()
        await ctx.send("Resumed playing.")
        print("Resumed playing.")
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")
        print("Tried to resume but no song was paused.")


@bot.command(name='stop', help='Stops the song')
async def stop(ctx: Context) -> None:
    global tasker
    global song_queue
    voice_client = ctx.message.guild.voice_client
    if voice_client and voice_client.is_playing():
        song_queue.clear()
        voice_client.stop()
        if tasker:
            tasker.cancel()
        await ctx.send("Stopped playing.")
        print("Stopped playing and cleared the queue.")
    else:
        await ctx.send("The bot is not playing anything at the moment.")
        print("Tried to stop but no song is playing.")


@bot.command(name='skip', help='Skip the song')
async def skip(ctx: Context) -> None:
    voice_client = ctx.message.guild.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Skipped song.")
        print("Skipped song.")
    else:
        await ctx.send("The bot is not playing anything at the moment.")
        print("Tried to skip but no song is playing.")

bot.run(__TOKEN__)
