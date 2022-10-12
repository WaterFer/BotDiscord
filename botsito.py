import discord
import requests


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message, user):
    await message.send("{0}".format(user)+", siuuuu")
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$cripto'):
        coin = message.content.split(' ')[1]
        divisa = message.content.split(' ')[2]
        info = requests.get(f'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={coin}&tsyms={divisa}')
        response = info.json()
        price = response['DISPLAY'][coin][divisa]['PRICE']
        high = response['DISPLAY'][coin][divisa]['HIGH24HOUR']
        low = response['DISPLAY'][coin][divisa]['LOW24HOUR']
        await message.channel.send(f'Moneda: {divisa}, crypto:{coin}')
        await message.channel.send(f'El precio es: {price}')
        await message.channel.send(f'El precio mas alto es: {high}')
        await message.channel.send(f'El precio mas bajo es: {low}')

    if message.content.startswith('$clima'):
        ciudad = message.content.split(' ')[1]
        info = requests.get(f'https://goweather.herokuapp.com/weather/{ciudad}')
        response = info.json()
        todayTemp = response['temperature']
        tomorrowTemp = response['forecast'][0]['temperature']
        tomorrow2Temp = response['forecast'][1]['temperature']
        await message.channel.send(f'Temperatura en {ciudad}')
        await message.channel.send(f'El dia de hoy es: {todayTemp}')
        await message.channel.send(f'El dia de mañana sera: {tomorrowTemp}')
        await message.channel.send(f'El dia de pasado mañana sera: {tomorrow2Temp}')


    if message.content.startswith('$info'):
        pais = message.content.split(' ')[1]
        info = requests.get(f'https://restcountries.com/v3.1/name/{pais}')
        response = info.json()
        name = response['name'][1]['common']
        await message.channel.send(f'func')

client.run('MTAyOTA4MDI3OTI1NzcyNzEzNw.GNhCfK.SuxnQBujqesOwr5PBXgX_HiNHCVjtja3RtAAoA')
