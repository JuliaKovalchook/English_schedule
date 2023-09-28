#!/usr/bin/env python
# coding: utf-8

# In[2]:


import json
import re
import pandas as pd
from datetime import datetime, timedelta


def get_date():

    f = open('chanel_messages.json')
    data = json.load(f)
    if len(data)==0:
        print('Don\'t have any data')
    else: print('Get %s rows' % len(data))




    df = pd.DataFrame(data)


    def set_event(row):
        if row["description"] == "https://t.me/mightofspeech":
            return "Might of Speech"
        elif row["description"] == "https://t.me/speaking_club_nice":
            return "Nice"
        elif row["description"] == "https://t.me/your_english_bro":
            return "English Bro"    
        else:
            return "speaking club"


    df = df.assign(event_name=df.apply(set_event, axis=1))
    df0=df[df['event_name']=='English Bro'].copy()
    return df0


def filter_bro(df0):

    '''
    Filter all message by pattern 

    pattern looks like #ДЕНЬ**: ПʼЯТНИЦЯ 08.09\n**ЧАС**: 15:00
    looking for "(16.09) о 12:00"  
    '''
    if len(df0)>0:
        pattern= re.compile("день.*\d{1,2}\.\d{1,2}.*\n.*час.*", re.IGNORECASE)  

        df0['message'] = df0['message'].apply(lambda x:  pattern.findall(str(x))).copy()
        df0=df0.explode('message') #if one message has several events, we separate them 
        df0.dropna(subset=['message'], inplace=True) #drop all rows wo information about event 
        df0=df0.reset_index(drop=True) 


        '''
        Change string with data to corect format
        '''

        df2=df0
        df2['start_event']=df2['message'].str.extract('(\d+\.\d+)', expand=True)+'.2023 '+\
                          df2['message'].str.extract('(\d+\:\d+)', expand=True)


        #df2['start_event'] = df2["start_event"].apply(lambda x: datetime.strptime(x, '%d.%m.%Y %H:%M').isoformat())
        df2['start_event'] = df2["start_event"].apply(lambda x: datetime.strptime(x, '%d.%m.%Y %H:%M')) #change to datatime
        #df2= df2[df2['start_event'] >= pd.to_datetime('today')] 
        df2['end_event'] = df2["start_event"].apply(lambda x: x + timedelta(hours=1)) #add 1 hours 


         #get current dateTime
        current_dateTime = pd.to_datetime('today')

        #filter by upcoming events only
        df_upcoming= df2[df2['start_event'] >= current_dateTime].copy()
       
        df_upcoming['start_event'] = df_upcoming["start_event"].apply(lambda x: (x.tz_localize('Europe/Kyiv')).isoformat()) #change to isoformat
        df_upcoming['end_event'] = df_upcoming["end_event"].apply(lambda x: (x.tz_localize('Europe/Kyiv')).isoformat())
        df_upcoming['location']='Ukraine'
        df_upcoming=df_upcoming[['event_name', 'description',  'start_event', 'end_event', 'location']]
    else:
        df_upcoming = pd.DataFrame(columns=['event_name', 'description', 'start_event','end_event','location'])
    return df_upcoming


#df0=get_date()
#df_upcoming=filter_bro(df0)

