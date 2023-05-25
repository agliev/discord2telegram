import requests
import json
import telebot
import pandas as pd
from secret import TOKEN
import snscrape.modules.telegram as telegramScarapper

headers = {'authorization':'NjkyNzc3NDQ2NDc0MjUyMzY5.GLdUpb.h8B5RbNqmxSqQSlkPBXL7_US8dmCzgvViQXEoE'}
channelId = '892124831343050775'

r = requests.get(f'https://discord.com/api/v9/channels/{channelId}/messages?limit=50', headers=headers)

jsonn = json.loads(r.text)

bot = telebot.TeleBot(TOKEN)

for value in jsonn[9::-1]:
    
    try:
        

        scrapper = telegramScarapper.Channel('-1615333169')
        mess_list = []

        for i, mydata in enumerate(scrapper.get_items()):
            if i>9:
                break
            mess_list.append(mydata)

        df = pd.DataFrame(mess_list)

        if value['content'] not in df['content']:
            bot.send_message('688962748', value['content'])
    
    except:
        pass


