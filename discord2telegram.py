from time import sleep
from random import random
import pandas as pd
from source import discord2telegram, get_gs_dis_channels


if __name__ == '__main__':
    
    while True:
        
        try:
            dis_channels_df = get_gs_dis_channels()

            for _, channel_data in dis_channels_df.iterrows():
                    
                    discord_name, dis_channel_name, dis_channel_url = channel_data
                    dis_channel_id = dis_channel_url.split('/')[-1]
                    print(discord_name, dis_channel_name)

                    discord2telegram(dis_channel_id, dis_channel_url, discord_name, dis_channel_name)
                    sleep(3+random())

        except:
            print('dis channels request failed')
    
        sleep(300+10*random())