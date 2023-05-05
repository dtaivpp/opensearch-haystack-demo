import os
from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv
from language_model import query_model

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
async def ask(ctx, *args):
    query = " ".join(args)
    response = query_model(query)
    await ctx.send(response)


if __name__=="__main__":
    client.run(discord_token)
