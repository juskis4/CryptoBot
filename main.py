import os
import discord
import requests
import json
import pprint
from replit import db



#getting crypto prices
def getCryptoPrices(crypto):
  URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=eur'
  r = requests.get(url = URL)
  data = r.json()

  #putting cryptocurrencies with their prices to a database
  for i in range(len(data)):
    db[data[i]['id']] = data[i]['current_price']
  
  if crypto in db.keys():
    return db[crypto]
  else:
    return None

def getCryptoChan
#function to check if crypto is in the database
def isCryptoSupported(crypto):
  if crypto in db.keys():
    return True
  else:
    return False

#instantiate a discord client
client = discord.Client()

@client.event
async def on_ready():
  print('You have logged in as {0.user}'.format(client))

#called when there is a message in the chat
@client.event
async def on_message(message):
  if message.author == client.user:
    return 

  if message.content.startswith('$hello'):
    embed=discord.Embed(title="Hello! :wave:", description="To get a list of my commands type $help", color=0x109319)
    await message.channel.send(embed=embed)

  #Gets the price of a crypto 
  if message.content.startswith('$price '):
    cryptoName = message.content.split('$price ',1)[1].lower()
    if isCryptoSupported(cryptoName):
      price = (f'The current price of **{cryptoName.capitalize()}** is: **{getCryptoPrices(cryptoName)}** EUR')
      embed=discord.Embed(title=cryptoName.capitalize(), description=price, color=0x109319)
      await message.channel.send(embed=embed)
    else:
      await message.channel.send('This crypto may be unsuported! Write $help for further instructions')

  #prints the supported crypto list
  if message.content.startswith('$list'):
    cryptoSupportedList = [key for key in db.keys()]
    await message.channel.send(cryptoSupportedList)

  #checks if a crypto is supported
  if message.content.startswith('$support '):
    cryptoToBeChecked = message.content.split('$support ',1)[1].lower()
    if isCryptoSupported(cryptoToBeChecked):
      await message.channel.send('Yes I do support this cryptocurrency!')
    else:
      await message.channel.send('Sorry but I am not aware of this cryptocurrency')
  #sends a list of commands
  if message.content.startswith('$help'):
    embed=discord.Embed(title="Commands :writing_hand:", description="Here is a list of commands I have:", color=0x109319)
    
    embed.add_field(name="$price cryptocurrency", value="Get the current price of a cryptocurrency you typed in", inline=True)

    embed.add_field(name="$list", value="Get a list of cryptocurrencies I support", inline=True)

    embed.add_field(name="$support cryptocurrency", value="Check if I support the cryptocurrency you typed in", inline=False)

    await message.channel.send(embed=embed)
  
            

my_secret = os.environ['password']
client.run(my_secret)



