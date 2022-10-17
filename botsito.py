from multiprocessing import connection
import discord
import requests

import sqlite3
connectionDB = sqlite3.connect("tutorial.db")
cur = connectionDB.cursor()


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
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

    if message.content.startswith('$info'):
        pais = message.content.split(' ')[1]
        info = requests.get(f'https://goweather.herokuapp.com/weather/{pais}')
        response = info.json()
        todayTemp = response['temperature']
        info_pais = requests.get(f'https://restcountries.com/v3.1/name/{pais}')
        response_pais = info_pais.json()
        name = response_pais[0]['name']['common']
        capital = response_pais[0]['capital'][0]
        population = response_pais[0]['population']
        region = response_pais[0]['region']
        bandera = response_pais[0]['flags']['png']
        await message.channel.send(f'<@{message.author.id}>, buscaste la informacion de {name}')
        await message.channel.send(f' Su capital es: {capital}')
        await message.channel.send(f'La temperatura es de {todayTemp}')
        await message.channel.send(f'Tiene una poblacion de {population} habitantes')
        await message.channel.send(f'Esta en la region de {region}')
        await message.channel.send(f'{bandera}')
        

    # if message.content.startswith('$info'):
    #     pais = message.content.split(' ')[1]
    #     info = requests.get(f'https://restcountries.com/v3.1/name/{pais}')
    #     response = info.json()
    #     name = response[0]['name']['common']
    #     await message.channel.send(f' {name}')

        if message.content.startswith('!CrearUsuario'):
            first_name = message.content.split(' ')[1]
            last_name = message.content.split(' ')[2]
            full_name = f'{first_name} {last_name}'
            cur.execute('INSERT INTO users (discord_id, name) VALUES (?, ?)', [message.author.id, full_name])
            connectionDB.commit()
            await message.channel.send('Usuario Creado!')

    if message.content.startswith('!BorrarUsuario'):
        cur.execute('DELETE FROM users WHERE discord_id = ?', [message.author.id])
        connectionDB.commit()
        await message.channel.send('Usuario Eliminado!')

client.run('MTAyOTA4MDI3OTI1NzcyNzEzNw.GY5W-v.kxRfgXiQBFbT_dZnpj-UoRxzEQ6vSvBRx-1OAA')
