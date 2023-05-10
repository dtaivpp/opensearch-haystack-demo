import os
from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv
from language_model import query_model
from time import time

# Load discord token for bot from .env file
load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')

intents = Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))


@client.command()
async def flan(ctx, *args):
    query = " ".join(args)
    start = time()
    response = query_model(query)
    end = time()
    response += f"\nTime Taken: {end - start}"
    await ctx.send(response)


@client.command()
async def gpt(ctx, *args):
    query = " ".join(args)
    start = time()
    response = query_model(query)
    end = time()
    response += f"\nTime Taken: {end - start}"
    await ctx.send(response)


if __name__=="__main__":
    client.run(discord_token)
