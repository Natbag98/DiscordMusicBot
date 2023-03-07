import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError
import asyncio


class MusicData(object):

    def __init__(self, data: dict):
        self.url = data['url']
        self.title = data['title']


class MusicCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        """
        A cog that connects to the users voice channel in discord, then plays music\n
        in that voice channel based on user input.
        """
        self.bot = bot

        self.voice_clients = {}
        self.ytdl_options = {'format': 'bestaudio/best'}
        self.ffmpeg_options = {'options': "-vn"}
        self.music_queue = []

    async def search(self, url: str) -> MusicData | str | None:
        """
        Search for a song on youtube with the given url.\n
        If an error occurs due to an incorrect url, then return a str instead of a MusicData object.
        """
        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: YoutubeDL(self.ytdl_options).extract_info(url, download=False))
            return MusicData(data)
        except DownloadError:
            return 'DownloadError'
        except Exception as error:
            print(error)

    async def play_song(self, ctx: Context, song: MusicData):
        player = discord.FFmpegPCMAudio(song.url, **self.ffmpeg_options, executable='C:\\ffmpeg\\ffmpeg.exe')
        self.voice_clients[ctx.author.guild.id].play(player)
        await ctx.send(f'Now playing: {song.title}')
        self.music_queue.remove(song)


async def setup(bot: commands.Bot):
    await bot.add_cog(MusicCog(bot))
