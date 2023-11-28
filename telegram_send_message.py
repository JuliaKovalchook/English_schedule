#!/usr/bin/env python
# coding: utf-8



from datetime import datetime, timedelta
import credentials_telegram
from telethon import TelegramClient
import os

def telegram_send_messages():
    api_id = int(credentials_telegram.api_id)
    api_hash = credentials_telegram.api_hash
    username = credentials_telegram.username
 
    client = TelegramClient(username, api_id, api_hash)
    client.start()
    
    time_message=datetime.now()
    running_file=os.path.basename(__file__)
    message_code='code works successfully' 
    message_status=time_message.strftime("%H:%M:%S %d-%m-%Y ") + '\n'+\
     running_file+ '\n\n' + message_code


    client.loop.run_until_complete(client.send_message(username, message_status))

telegram_send_messages()
