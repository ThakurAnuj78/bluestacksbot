import discord
import os
from utils import google_search, recent_search
from database import mydatabase


dbms = mydatabase.MyDatabase(mydatabase.SQLITE, dbname='mydb.sqlite')
dbms.create_db_tables()

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

    author = message.author
    if author == client.user:
        return

    contents = message.content.split(" ")
    if len(contents) > 1:
        if contents[0].startswith('!google'):
            await message.channel.send(google_search(" ".join(contents[1:]), dbms))
        elif contents[0].startswith('!recent'):
            await message.channel.send(recent_search(" ".join(contents[1:]), dbms))

client.run(os.getenv('TOKEN'))