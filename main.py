import os
import discord
import requests
import json
import pprint
from replit import db


#function used to get a 24h change percentage of a crypto price
def get24hChange(crypto):
  URL = 'https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies=eur&include_market_cap=false&include_24hr_vol=false&include_24hr_change=true&include_last_updated_at=false'.format(crypto)
  r = requests.get(url = URL)
  data = r.json()
  data = data[crypto]
  change = data['eur_24h_change']
  return round(change, 2)

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
      change = get24hChange(cryptoName)
      #Changes the color of a message depending if the price went up or down in 24hours
      if change > 0:
        color = 0x1aff00 #green
      else:
        color = 0xff0000 #red

      price = (f'The current price of **{cryptoName.capitalize()}** is: **{getCryptoPrices(cryptoName)}** EUR')

      embed=discord.Embed(title=cryptoName.capitalize(), description=price, color=color)
      embed.add_field(name ="--------------------------------------------", value="**24 Hour change:** {}%".format(change))
      await message.channel.send(embed=embed)

    else:
      embed=discord.Embed(title="Error", description="This crypto may be unsuported! Write $help for further instructions", color=0x109319)
      await message.channel.send(embed=embed)

  #checks if a crypto is supported
  if message.content.startswith('$support '):
    cryptoToBeChecked = message.content.split('$support ',1)[1].lower()
    if isCryptoSupported(cryptoToBeChecked):
      embed=discord.Embed(title="Do I support it?", description="Yes I do support {}!".format(cryptoToBeChecked), color=0x109319)
      await message.channel.send(embed=embed)
    else:
      embed=discord.Embed(title="Do I support it?", description="Sorry but I do not support {}".format(cryptoToBeChecked), color=0x109319)
      await message.channel.send(embed=embed)

  #sends a list of commands
  if message.content.startswith('$help'):
    embed=discord.Embed(title="Commands :writing_hand:", description="Here is a list of commands I have:", color=0x109319)
    
    embed.add_field(name="$price cryptocurrency", value="Get the current price of a cryptocurrency you typed in", inline=False)

    embed.add_field(name="$list", value="Get a list of cryptocurrencies I support", inline=False)

    embed.add_field(name="$support cryptocurrency", value="Check if I support the cryptocurrency you typed in", inline=False)

    await message.channel.send(embed=embed)
  
            

my_secret = os.environ['password']
client.run(my_secret)



