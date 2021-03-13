
import os
import random
import json

import discord
from discord.ext import commands

import psycopg2
from dotenv import load_dotenv

# Environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
HOST = os.getenv('POSTGRES_HOST')
USER = os.getenv('POSTGRES_USER')
PASSWORD = os.getenv('POSTGRES_PASSWORD')
DATABASE = os.getenv('POSTGRES_DATABASE')

# List of roles that can use the commands
mod_roles = []

# Database statements
insert = 'INSERT INTO public.warning(id, name, enforcer, reason, server) VALUES(%s, %s, %s, %s, %s);'
query = 'SELECT enforcer, reason, warned_on FROM public.warning where id = %s AND server = %s ORDER BY warned_on DESC'
query_all = 'SELECT id, name FROM public.warning where server = %s;'

# Bot command
bot = commands.Bot(command_prefix='~')

# Database connection
conn = None

# Try connecting to database
try:
    conn = psycopg2.connect(host=HOST, database=DATABASE,
                            user=USER, password=PASSWORD)
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
    quit()

# Double check connection
if conn is None:
    print("Connection is null")
    quit()


@bot.command(name='warn', help='Give a warning to user')
@commands.has_any_role(*mod_roles)
async def warn(ctx, user: discord.User, *, reason):
    # Check is user has the ROLE role
    for role in user.roles:
        if role.name in mod_roles:
            await ctx.send('You can not warn a mod.')
            return

    # Max character count for reason is 180 characters
    if len(reason) > 180:
        await ctx.send('Reason exceeds the 180 max character limit')
        return

    # Insert warning to database
    cur = conn.cursor()
    cur.execute(insert, (user.id, user.name, ctx.author.name, reason, str(ctx.guild.id),))
    conn.commit()

    # Send confirmation message
    await ctx.send(f'{user.name} has been warned for {reason}')


@bot.command(name='get_warnings', help='Lists all warnings to a user')
@commands.has_any_role(*mod_roles)
async def get_warnings(ctx, user: discord.User):
    # Get warnings for user from database
    cur = conn.cursor()
    cur.execute(query, (str(user.id), str(ctx.guild.id),))

    # Check if there are rows from query
    if cur.rowcount < 1:
        # If no rows then user has not been warned
        await ctx.send(f'{user.name} has not been warned')
    else:
        # Create embed to send data
        warnings = discord.Embed(
            title=f'Warnings for {user.name}',
            colour=discord.Colour.blue()
        )

        # Create new field for every row
        for warning in cur:
            warnings.add_field(
                name=f'on {warning[2]} by {warning[0]}', value=warning[1], inline=False)

        # Send warnings back in embedded message
        await ctx.send(embed=warnings)


@bot.command(name='get_all', help='Lists all users that have warnings')
@commands.has_any_role(*mod_roles)
async def get_all(ctx):
    # Get all warnings form database
    cur = conn.cursor()
    cur.execute(query_all, (str(ctx.guild.id),))

    # Check if there are rows
    if cur.rowcount < 1:
        # If no rows then no one has been warned
        await ctx.send('No one has been warned yet.')
    else:
        # Craete object to save user names and warning count
        users = {}

        # Get warning count for every user
        for warning in cur:
            if warning[0] not in users:
                users[warning[0]] = {}
                users[warning[0]]['name'] = warning[1]
                users[warning[0]]['count'] = 1
            else:
                users[warning[0]]['count'] = users[warning[0]]['count'] + 1

        # Create strings of every name and their count sperated by new line
        names = ''
        counts = ''
        for u in users:
            names = names + users[u]['name'] + '\n'
            counts = counts + str(users[u]['count']) + '\n'

        # Create embed object to send back all warned people.
        warnings = discord.Embed(
            title='Warned People',
            colour=discord.Colour.blue()
        )
        warnings.add_field(name='name', value=names, inline=True)
        warnings.add_field(name='# of warnings', value=counts, inline=True)

        # Send bcak all warned people in embedded message
        await ctx.send(embed=warnings)


@bot.event
async def on_command_error(ctx, error):
    print(error)
    # with open('err.log', 'w+') as e:
    #     e.write(error + '\n')

bot.run(TOKEN)
