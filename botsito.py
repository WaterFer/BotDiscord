import discord
import requests
import os
from dotenv import load_dotenv
load_dotenv()


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

    if message.content.startswith('$help'):
        await message.channel.send(f"""
         Hola, <@{message.author.id}>, esta es la lista de comandos que se pueden usar en este Bot ACTUALMENTE.
        -Para usar la Calculadora se debe poner **$calc** y la operación.
        -Para usar el cotizador de CriptoMonedas se debe poner **$crypto** más la cripto y la divisa.
        -Para ver el clima de los paises y ciudades se debe poner **$clima** y el nombre del país o ciudad.
        -Para ver información de los paises **$info** y el nombre del país.
        -Para obtener la información de los jugadores de la MLB se debe poner **$jugador** más el nombre y apellido.
        -Para obtener las estadisticas por año de los jugadores de la MLB se debe poner **$stats** más el nombre, el apellido y el año.
        -Para obtener las estadisticas de toda la trayectoria de los jugadores de la MLB se debe poner **$trayectory** más el nombre, el apellido del jugador.
        """)

        # Calculadora
    if message.content.startswith('$calc'):
        operacion = message.content.split (' ')[1]

        def calc(op):
            if op.__contains__('+'):
                num1 = int(op.split('+')[0])
                num2 = int(op.split('+')[1])
                return num1 + num2;
            elif op.__contains__('-'):
                num1 = int(op.split('-')[0])
                num2 = int(op.split('-')[1])
                return num1 - num2;
            elif op.__contains__('x'):
                num1 = int(op.split('x')[0])
                num2 = int(op.split('x')[1])
                return num1 * num2;
            elif op.__contains__('/'):
                num1 = int(op.split('/')[0])
                num2 = int(op.split('/')[1])
                return num1 / num2;
            else:
                return 'Ha habido un error'
        resultado = calc(operacion);

        await message.channel.send(f'Hola <@{message.author.id}>')
        await message.channel.send(f'el resultado es: {resultado}')

        # Cotizador de criptos
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


        # clima
    if message.content.startswith('$clima'):
        ciudad = message.content.split(' ')[1]
        info = requests.get(f'https://goweather.herokuapp.com/weather/{ciudad}')

        response = info.json()
        todayTemp = response['temperature']
        tomorrowTemp = response['forecast'][0]['temperature']
        tomorrow2Temp = response['forecast'][1]['temperature']

        await message.channel.send(f'Temperatura en: {ciudad}')
        await message.channel.send(f'El dia de hoy es: {todayTemp}')
        await message.channel.send(f'El dia de mañana sera: {tomorrowTemp}')
        await message.channel.send(f'El dia de pasado mañana sera: {tomorrow2Temp}')


        # informancion de los paises
    if message.content.startswith('$info'):


        if len(message.content) > 5:
            pais = message.content.split(' ')[1]
            info = requests.get(f'https://goweather.herokuapp.com/weather/{pais}')
            response = info.json()
            temperatura = response['temperature']
            clima = response['description']
            info_pais = requests.get(f'https://restcountries.com/v3.1/name/{pais}')
            response_pais = info_pais.json()
            name = response_pais[0]['name']['common']
            capital = response_pais[0]['capital'][0]
            population = response_pais[0]['population']
            region = response_pais[0]['region']
            flags = response_pais[0]['flags']['png']


            await message.channel.send(f'<@{message.author.id}>, buscaste la información de {name}')
            await message.channel.send(f' Su capital es : {capital}')
            await message.channel.send(f'La temperatura es de {temperatura}')
            await message.channel.send(f'El clima es : {clima}')
            await message.channel.send(f'Tiene una población de {population} de habitantes')
            await message.channel.send(f'Esta en la región de {region}')
            await message.channel.send(f'{flags}')

        else:


            info_ip = requests.get(f'https://api.geoapify.com/v1/ipinfo?apiKey=b49dd1f965654ae591d926ec01b31d19')
            response = info_ip.json()
            country_ip = response['country']['names']['de']
            temp = requests.get(f'https://goweather.herokuapp.com/weather/{country_ip}')
            response_temp = temp.json()
            temperatura = response_temp['temperature']
            clima = response_temp['description']
            info_pais = requests.get(f'https://restcountries.com/v3.1/name/{country_ip}')
            response_pais = info_pais.json()
            name = response_pais[0]['name']['common']
            capital = response_pais[0]['capital'][0]
            population = response_pais[0]['population']
            region = response_pais[0]['region']
            flags = response_pais[0]['flags']['png']


            await message.channel.send(f'<@{message.author.id}>, esta es la información de {name}')
            await message.channel.send(f' Su capital es: {capital}')
            await message.channel.send(f'La temperatura es de {temperatura}')
            await message.channel.send(f'El clima es : {clima}')
            await message.channel.send(f'Tiene una población de {population} de habitantes')
            await message.channel.send(f'Esta en la región de {region}')
            await message.channel.send(f'{flags}')


        # Baseball information
            # informacion de jugador de baseball
    def JugadorID(full_name):
        info = requests.get(f'https://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code=%27&name_part=%27{full_name}%25%27')
        responseIp = info.json()
        JugadorID = responseIp['search_player_all']['queryResults']['row']['player_id']
        return JugadorID


    if message.content.startswith('$jugador'):
        nameJugador = message.content.split(' ')[1]
        lastJugador = message.content.split(' ')[2]
        full_name = f'{nameJugador} {lastJugador}'

        info = requests.get(f'https://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code=%27&name_part=%27{full_name}%25%27')
        responseIp = info.json()
        JugadorID = responseIp['search_player_all']['queryResults']['row']['player_id']
        FotoJ = f"https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/{JugadorID}/headshot/67/current"

        infoJugador = requests.get(f"http://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code='mlb'&player_id='{JugadorID}'")
        responseJugador = infoJugador.json()

        Jugador = responseJugador['player_info']['queryResults']['row']['name_display_last_first']
        Nacionalidad = responseJugador['player_info']['queryResults']['row']['birth_country']
        Nacimiento = responseJugador['player_info']['queryResults']['row']['birth_date']
        Ciudad = responseJugador['player_info']['queryResults']['row']['birth_city']
        Altura = responseJugador['player_info']['queryResults']['row']['height_feet']
        Edad = responseJugador['player_info']['queryResults']['row']['age']
        Peso = responseJugador['player_info']['queryResults']['row']['weight']
        EquipoActual = responseJugador['player_info']['queryResults']['row']['team_name']
        bateo = responseJugador['player_info']['queryResults']['row']['bats']
        posicion = responseJugador['player_info']['queryResults']['row']['primary_position_txt']
        debut = responseJugador['player_info']['queryResults']['row']['pro_debut_date']

        date = Nacimiento.split('T')[0]
        date_debut = debut.split('T')[0]
        #weight in kg
        weight_kg = int(Peso) / 2.205
        kg_round = round(weight_kg, 2)
        #height in m
        height_m = int(Altura) / 3.281
        m_round = round(height_m, 2)


        await message.channel.send(f'{FotoJ}')
        await message.channel.send(f'Apellido, Nombre: {Jugador}')
        await message.channel.send(f'Nacionalidad: {Nacionalidad}')
        await message.channel.send(f'Es de la ciudad de {Ciudad}')
        await message.channel.send(f'Nació el {date}')
        await message.channel.send(f'Tiene {Edad} Años')
        await message.channel.send(f'Mide {m_round}m')
        await message.channel.send(f'Pesa {kg_round}Kg')
        await message.channel.send(f'Actualmente juega con los {EquipoActual}')
        await message.channel.send(f'Debuto el {date_debut}')
        await message.channel.send(f'Batea en el perfil {bateo}')
        await message.channel.send(f'Juega en {posicion}')

        # estadisticas del jugador
    if message.content.startswith('$stats'):

        nameJugador = message.content.split(' ')[1]
        lastJugador = message.content.split(' ')[2]
        year =  message.content.split(' ')[3]
        full_name = f'{nameJugador} {lastJugador}'
        result_id = JugadorID(full_name)
        FotoJ = f"https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/{result_id}/headshot/67/current"
        details = requests.get(f"http://lookup-service-prod.mlb.com/json/named.sport_hitting_tm.bam?league_list_id='mlb'&game_type='R'&season='{year}'&player_id='{result_id}'")
        response_career = details.json()

        Hits = response_career['sport_hitting_tm']['queryResults']['row']['h']
        HomeRun = response_career['sport_hitting_tm']['queryResults']['row']['hr']
        Carreras = response_career['sport_hitting_tm']['queryResults']['row']['r']
        Ponches = response_career['sport_hitting_tm']['queryResults']['row']['so']
        BasexBola = response_career['sport_hitting_tm']['queryResults']['row']['bb']
        Avg = response_career['sport_hitting_tm']['queryResults']['row']['avg']
        TurnoAlBate  = response_career['sport_hitting_tm']['queryResults']['row']['ab']
        Jjugados = response_career['sport_hitting_tm']['queryResults']['row']['g']
        CarreraImpulsada = response_career['sport_hitting_tm']['queryResults']['row']['rbi']
        Season = response_career['sport_hitting_tm']['queryResults']['row']['season']

        await message.channel.send(f'{FotoJ}')
        await message.channel.send(f'Temporada: {Season}')
        await message.channel.send(f'Juegos jugados: {Jjugados} ')
        await message.channel.send(f'Turnos al bate: {TurnoAlBate}')
        await message.channel.send(f'Carreras: {Carreras}')
        await message.channel.send(f'Hits: {Hits}')
        await message.channel.send(f'Carrara impulsada: {CarreraImpulsada}')
        await message.channel.send(f'Base por bola: {BasexBola}')
        await message.channel.send(f'Ponches: {Ponches}')
        await message.channel.send(f'HomeRuns: {HomeRun}')
        await message.channel.send(f'PRO: {Avg}')

    if message.content.startswith('$trayectory'):
        nameJugador = message.content.split(' ')[1]
        lastJugador = message.content.split(' ')[2]
        full_name = f'{nameJugador} {lastJugador}'
        result_id = JugadorID(full_name)
        FotoJ = f"https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/{result_id}/headshot/67/current"
        details = requests.get(f"http://lookup-service-prod.mlb.com/json/named.sport_career_hitting.bam?league_list_id='mlb'&game_type='R'&player_id='{result_id}'")
        response_career = details.json()

        Hits = response_career['sport_career_hitting']['queryResults']['row']['h']
        HomeRun = response_career['sport_career_hitting']['queryResults']['row']['hr']
        Carreras = response_career['sport_career_hitting']['queryResults']['row']['r']
        Ponches = response_career['sport_career_hitting']['queryResults']['row']['so']
        BasexBola = response_career['sport_career_hitting']['queryResults']['row']['bb']
        Avg = response_career['sport_career_hitting']['queryResults']['row']['avg']
        TurnoAlBate  = response_career['sport_career_hitting']['queryResults']['row']['ab']
        Jjugados = response_career['sport_career_hitting']['queryResults']['row']['g']
        CarreraImpulsada = response_career['sport_career_hitting']['queryResults']['row']['rbi']

        await message.channel.send(f'{FotoJ}')
        await message.channel.send(f'Juegos jugados: {Jjugados} ')
        await message.channel.send(f'Turnos al bate: {TurnoAlBate}')
        await message.channel.send(f'Carreras: {Carreras}')
        await message.channel.send(f'Hits: {Hits}')
        await message.channel.send(f'Carreras impulsadas: {CarreraImpulsada}')
        await message.channel.send(f'Bases por bola: {BasexBola}')
        await message.channel.send(f'Ponches: {Ponches}')
        await message.channel.send(f'HomeRuns: {HomeRun}')
        await message.channel.send(f'PRO: {Avg}')

    if message.content.startswith('$team'):
        nameTeam = message.content.split(' ')[1]




client.run(os.environ['TOKEN'])
