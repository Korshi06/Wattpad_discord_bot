import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
from gtts import gTTS


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('DISCORD_CHANNEL')

client = commands.Bot(command_prefix=">>>", intents=discord.Intents.all())


@client.event
async def on_ready():

    guild = discord.utils.get(client.guilds, name=GUILD)

    print(f'{client.user} has connected to Discord!\n'
          f'{guild.name}(id: {guild.id})')

    if guild:
        channel = discord.utils.get(guild.text_channels, name=CHANNEL)
        if channel:
            await channel.send(
                'WattpadBOT has connected to Discord!\n\n'
                'Use: ```>>>generate [url] [fileName] [lang]``` to generate mp3 files from Wattpad chapters'
            )
        else:
            print(f"Channel '{CHANNEL}' not found in guild '{GUILD}'.")
    else:
        print(f"Guild '{GUILD}' not found.")


@client.command()
async def hello(ctx):
    await ctx.send('Hello there!')


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}


def getData(url):
    print('Getting data from: ' + url)
    r = requests.get(url, headers=HEADERS)
    return r.text


@client.command()
async def helpMe(ctx):
    await ctx.send('use: >>>generate [url] [fileName] [lang] to generate mp3 files from wattpad chapters')


@client.command()
async def generate(ctx, url, fileName='chapter', lang='en'):

    if 'https://www.wattpad.com' not in url:
        await ctx.send('Invalid URL')
        return

    chapter = ''
    await ctx.send('Looking for: ' + url)
    html = getData(url)
    soup = BeautifulSoup(html, 'html.parser')
    await ctx.send('Data found!, generating...')

    for data in soup.find_all('p', {'data-p-id': True}):
        print(data.text)
        if data.text != '':
            chapter += data.text + '\n'

    if chapter:
        tts = gTTS(chapter, lang=lang, slow=False)
        tts.save(fileName + ".mp3")
        await ctx.send('Chapter generated!')
        await ctx.send(file=discord.File(fileName + '.mp3'))

        try:
            if os.path.exists(fileName + ".mp3"):
                os.remove(fileName + ".mp3")
                print('Text file deleted successfully.')
            else:
                print('Text file does not exist.')
        except Exception as e:
            await print(f'Error deleting file: {e}')


client.run(TOKEN)
