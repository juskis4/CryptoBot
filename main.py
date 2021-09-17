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
    await message.channel.send('Hello!')

  #Gets the price of a crypto 
  if message.content.lower() in db.keys():
    await message.channel.send(f'The current price of {message.content} is: {getCryptoPrices(message.content.lower())} EUR')
  #prints the supported crypto list
  if message.content.startswith('$list'):
    cryptoSupportedList = [key for key in db.keys()]
    await message.channel.send(cryptoSupportedList)
  #checks if a crypto is supported
  if message.content.startswith('$support '):
    cryptoToBeChecked = message.content.split('$support ',1)[1].lower()
    await message.channel.send(isCryptoSupported(cryptoToBeChecked))
  
            

my_secret = os.environ['password']
client.run(my_secret)



