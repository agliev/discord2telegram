import re
import requests
import json
import telebot
import gspread
import pandas as pd
from time import sleep
from secret import TOKEN
from random import random
from secret import telegram_channel_id, headers
import snscrape.modules.telegram as telegramScarapper



def get_gs_dis_channels():

    sa = gspread.service_account('dis2tel-380920-482b89db1796.json')
    sh = sa.open("discord_channels")

    discord_channels = sh.worksheet('discord_channels')
    df = pd.DataFrame(discord_channels.get_all_records())
    
    return df


def discord2telegram(dis_channel_id:str,
                     dis_channel_url:str,
                     dis_name:str,
                     dis_channel_name:str, 
                     token:str=TOKEN,
                     headers:dict=headers):

    try:
        r = requests.get(f'https://discord.com/api/v9/channels/{dis_channel_id}/messages?limit=50', headers=headers)

        jsonn = json.loads(r.text)

        bot = telebot.TeleBot(token)

        for value in jsonn[:3]:
            
            scrapper = telegramScarapper.TelegramChannelScraper('discord2telegram')
            

            try:
                mess_list = [mess for _, mess in enumerate(scrapper.get_items())]

                channel_mess_df = pd.DataFrame(mess_list)

                message_pattern = f'*Discord name*: {dis_name}\n*Discord_channel_name*: [{dis_channel_name}]({dis_channel_url})\n\n*Message content*: '
                message_content =  re.sub(r'<.*?>','', value['content'])
                full_message = message_pattern + message_content

                # message_pattern_mod = message_pattern.replace('*','').replace('\n','').replace('[','').replace(']','').replace(f'({dis_channel_url})','')
                full_message_mod = full_message.replace('*','').replace('\n','').replace('[','').replace(']','').replace(f'({dis_channel_url})','').replace(' ','').replace('_','').replace(' ','')
                
                if full_message_mod not in set(channel_mess_df['content'].apply(lambda x: re.sub(r'<.*?>',' ', x).replace(' ','').replace('_','').replace("\u2028",'').replace('[','').replace(']',''))):

                    if len(message_content) > 0:
                        bot.send_message(telegram_channel_id, full_message, parse_mode= 'Markdown')

                        sleep(0.05+0.1*random())
                        print(f'Message sent - {value["content"]}...')
                        
                                            
                else:
                    pass
            
            except:
                print('Error!')
    except:
        print(f"Does this discord channel exist? - {dis_name} {dis_channel_name}")
