#!/usr/bin/python3

# bot.py
import os
import asyncio
import discord
import urllib.request
import re
import random
import unicodedata
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from discord.ext.commands import Bot
from collections import deque
from pretty_help import PrettyHelp
from fuzzywuzzy import fuzz
from difflib import SequenceMatcher

load_dotenv('postavke.env')
token = os.getenv('BOT_TOKEN')
server = os.getenv('DISCORD_SERVER')
PATH = os.getenv('FILE_PATH')

svirac = Bot(command_prefix='<', help_command=PrettyHelp(no_category="Help", show_index=False))
q = deque()
sviram = ' '

def matcher(a, b):
    if len(b) < 10:
        return (SequenceMatcher(None, a, b).ratio(), 0.65 * pow(1.005, len(b)-6))
    else:
        return (fuzz.partial_ratio(a, b)/100, 0.8) 

#muzika s interneta
def download(upis):
    trazi = "https://www.youtube.com/results?search_query="
    query = upis.replace(" ", "+")
    trazi = trazi + query
    trazi = str(trazi.encode('utf-8').decode('ascii', 'ignore'))
    print(trazi)

    html = urllib.request.urlopen(trazi)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    rezultat = "https://www.youtube.com/watch?v=" + video_ids[0]

    naredba = 'yt-dlp -x --audio-format mp3 --output "' + PATH + upis + '.mp3" ' + rezultat

    os.system(naredba)
    print('Skinuto je')

#kju
def muzika(vc):
    global q
    global sviram

    if len(q) > 0 and not vc.is_playing():
        sviram = q.popleft()
        pesma = sviram + ".mp3"
        pesma = PATH + pesma
        print('Trebal bi svirati ' + pesma + ' ' + str(len(pesma)))
        vc.play(discord.FFmpegOpusAudio(pesma), after=lambda m: muzika(vc))

    return

#spajanje na server
@svirac.event
async def on_ready():
    for guild in svirac.guilds:
        if guild.name == server:
             break
    print(
        f'{svirac.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

#muzika s kompa
@svirac.command(name='sviraj', help='svira muziku s kompjutera')
async def sviraj(ctx, *ime):
    channel = ctx.message.author.voice.channel
    try: await channel.connect()
    except:
        vc = ctx.voice_client
        print('Already connected.')
        if vc.is_playing():
            await ctx.send('Sviram pesmu ' + sviram)

    fajlq = ime[0]
    duljina = len(ime)
    for x in range(1,duljina):
        fajlq = fajlq + ' ' + ime[x]

    pesma = fajlq + ".mp3"
    #fajl postoji
    if os.path.exists(PATH + pesma):
        pesma = PATH + pesma
        q.append(fajlq)
    else:
        #fajl ne postoji
        najmanja = -1 #razlika najblizeg
        fajl = ' ' #ime najblizeg

        os.system('ls ' + PATH + ' > ' + PATH + 'popis.txt')
        file = open(PATH + "popis.txt", "r")
        kriterij = 0
        for x in file:
            match_result = matcher(pesma[:len(pesma)-4].lower(), x[:len(x)-4].lower())
            distanca = match_result[0]
            if(distanca > najmanja):
                najmanja = distanca
                kriterij = match_result[1]
                fajl = x

        if najmanja > kriterij:
            fajl = fajl[:len(fajl)-5]
            q.append(fajl)
        else:
            while not os.path.exists(PATH + pesma):
                download(fajlq)
            await ctx.send('Skinuto je.')
            q.append(fajlq)


    vc = ctx.voice_client
    await ctx.send('Dodana je pesma ' + q[-1])
    
    if not vc == None:
        muzika(vc)


#pauziranje
@svirac.command(name='pauza', help='pauira muziku')
async def pauziraj(ctx):
    vc = ctx.voice_client
    try: vc.pause()
    except:
        response = 'Vec je pauzirano. Jebo ti pas mater glupu'
        await ctx.send(response)

#resume
@svirac.command(name='nastavi', help='nastavlja muziku nakon pauziranja')
async def nastavak(ctx):
    vc = ctx.voice_client
    try: vc.resume()
    except:
        response = 'Nikaj je ne pauzirano. Naj me jebati'
        await ctx.send(response)

#skip
@svirac.command(name='skip', help='preskace trenutni track')
async def skip(ctx):
    vc = ctx.voice_client
    try: vc.stop()
    except:
        response = 'Nist ne sviram'
        await ctx.send(response)

#remove from queue
@svirac.command(name='remove', help='brise pesmu sa kjua (index obavezan)')
async def remove(ctx, *imena):
    upis = imena[0]
    for x in range(1,len(imena)):
        upis = upis + ' ' + imena[x]
    try:
        q.remove(upis)
        response = 'Maknul sam pesmu ' + upis
        await ctx.send(response)
    except:
        response = 'Nema pesme na tom mestu u kjuu'
        await ctx.send(response)

#disconnect
@svirac.command(name='disconnect', help='diskonektuje sa servera')
async def disconnect(ctx):
    try:
        kanal = ctx.voice_client.channel
        await ctx.voice_client.disconnect()
    except:
        await ctx.send('Nisam spojen. Koji ti je kurac?')

@svirac.command(name='lista', help='ispisuje kaj je na listi')
async def lista(ctx):
    response = ''
    for x in range(0,len(q)):
        response = response + str(x+1) + " " + q[x] + '\n'
    embed = discord.Embed(title="Kju pesama", description=response, color=discord.Color.red())
    await ctx.send(embed=embed)


@svirac.command(name='miks', help='shuffle')
async def miks(ctx):
    global q
    random.shuffle(q)

@svirac.command(name='clear', help='klira kju')
async def klir(ctx):
    global q
    q.clear()
    vc = ctx.voice_client
    try: vc.stop()
    except:
        response = 'Nist ne sviram'
        await ctx.send(response)

@svirac.command(name='popis', help='ispisuje popis mogucih pesama')
async def popis(ctx, slovo):
    os.system('ls ' + PATH + ' > ' + PATH + 'popis.txt')
    file = open(PATH + "popis.txt", "r")
    ispis = ''
    for x in file:
        if x[0] == slovo.lower() or x[0] == slovo.upper():
            ispis = ispis + x + '\n'

    embed = discord.Embed(title="Popis pesama", description=ispis, color=discord.Color.blue())
    await ctx.send(embed=embed)

@svirac.command(name='download', help='skida pesmu s interneta')
async def skini(ctx, *upis):
    pjesma = upis[0]
    for x in range(1,len(upis)):
        pjesma = pjesma + ' ' + upis[x]
    while not os.path.exists(PATH + pjesma + ".mp3"):
        download(pjesma)
    await ctx.send('Skinuto je.')

@svirac.command(name='now', help='ispisuje trenutnu pesmu')
async def now(ctx):
    vc = ctx.voice_client
    if vc.is_playing():
        await ctx.send('Sviram pesmu ' + sviram)
    else:
        await ctx.send('Ne sviram nikaj. Koji ti je kurac?')

@svirac.command(name='ladd', help='stavlja pesmu na odabranu playlistu (upisite ime liste pa zatim ime pesme)')
async def ladd(ctx, list, *args):
    upis = args[0]
    for x in range(1, len(args)):
        upis = upis + ' ' + args[x]

    fajl2 = open(PATH + list + ".txt", "a+")

    if os.path.exists(PATH + upis + ".mp3"):
        pesma = PATH + upis + ".mp3"
        fajl2.write(upis + "\n")
        await ctx.send('Stavljena je pesma ' + upis + ' na listu ' + list)
    else:
        #fajl ne postoji
        najmanja = -1 #razlika najblizeg
        fajl = ' ' #ime najblizeg

        os.system('ls ' + PATH + ' > ' + PATH + 'popis.txt')
        file = open(PATH + "popis.txt", "r")
        kriterij = 0
        for x in file:
            match_result = matcher(None, upis.lower(), x[:len(x)-4].lower())
            distanca = match_result[0]
            if(distanca > najmanja):
                najmanja = distanca
                kriterij = match_result[1]
                fajl = x

        if najmanja > kriterij:
            fajl = fajl[:len(fajl)-5]
            fajl2.write(fajl + "\n")
            await ctx.send('Stavljena je pesma ' + fajl + ' na listu ' + list)
        else:
            while not os.path.exists(PATH + upis + ".mp3"):
                download(upis)
            await ctx.send('Skinuto je.')
            fajl2.write(upis + "\n")
            await ctx.send('Stavljena je pesma ' + upis + ' na listu ' + list)

@svirac.command(name='lplay', help='stavlja odabranu listu na kju')
async def lplay(ctx, list):
    channel = ctx.message.author.voice.channel
    try: await channel.connect()
    except:
        vc = ctx.voice_client
        print('Already connected.')
        if vc.is_playing():
            await ctx.send('Sviram pesmu ' + sviram)

    fajl = open(PATH + list + ".txt", "r")
    for x in fajl:
        q.append(x[:len(x)-1])

    vc = ctx.voice_client
    muzika(vc)

#aktivira svirace na svirku
svirac.run(token)
