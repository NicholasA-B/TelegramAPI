from requests import Request, Session
import json
import pprint
import datetime
import telebot
from telebot.types import Chat, Message
import math
import dateutil.parser

bot = telebot.TeleBot('1989916503:AAFaOfSDCGZX1JkigxT8ANPoG_rFpPZ_HU4')


def get_data():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
            
    parameters = {
        'sort':'date_added',
        'limit':'10'
    }

    headers = {
        'Accepts':'application/json',
        'X-CMC_PRO_API_KEY':'482975e5-8857-4b8e-87ac-86f085243ce8'
    }

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)

    data = json.loads(response.text)

    return data

class Coin:
    def __init__(self):
        self.name = []
        self.symbol = []
        self.price = []
        self.date_added = []
        

    def store_values(self, data):
        for i in range(10):
            self.name.append(data['data'][i]['name'])
            self.symbol.append(data['data'][i]['symbol'])
            self.price.append(data['data'][i]['quote']['USD']['price'])
            self.date_added.append(data['data'][i]['date_added'])

    def get_values(self):
        file = open('coin_data.txt', '+w')
        file.write("10 Most Recent Coins:\n\n")  
        for i in range(10):
            d = dateutil.parser.parse(self.date_added[i])
            file.write(f"{i+1}. {self.name[i]} ({self.symbol[i]})\n Price: ${round(self.price[i], 10)}\n Added On: {d.strftime('%m/%d/%Y %H:%M')}\n\n")
        file.close()

if __name__ == '__main__':
    print("Beep Boop Bop Bop...")


@bot.message_handler(commands=['new'])
def get_recent(message):    
    coin = Coin()
    data = get_data()
    coin.store_values(data)
    coin.get_values()
    
    with open('coin_data.txt', 'r') as file:
        lines = file.read()
    
    bot.reply_to(message, lines)

bot.polling()

