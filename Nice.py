#!/usr/bin/env python
# coding: utf-8



import json
import re
import pandas as pd
from datetime import datetime, timedelta
#import numpy as np

events_name='Nice'
def get_date(events_name):

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
    df0=df[df['event_name']==events_name].copy()
    return df0

def filter_nice(df0):

    '''
    Filter all message by pattern 

    pattern looks like #Безкоштовний спікінг клаб буде завтра (16.09) о 12:00 
    looking for "(16.09) о 12:00"  
    '''
    if len(df0)>0:
        df=df0
        pattern= re.compile("\(\d{1,2}\.\d{1,2}\)\s+о\s+\d{1,2}:\d{1,2}") 
        df['message'] = df['message'].apply(lambda x: pattern.findall(str(x))) 
        df=df.explode('message') #if one message has several events, we separate them 
        df.dropna(subset=['message'], inplace=True) #drop all rows wo information about event 
        df=df.reset_index(drop=True) 

        '''
        Change string with data to corect format
        '''

        df2=df.copy()
        df2['event_date']=df2['message'].str.replace('(\s+о\s+)(\d{1,2}:\d{1,2})', '', regex=True)\
                                        .str.replace('\(|\)', '', regex=True)+'.2023' #get date (first replace all not date, after relcae () after add year)

        df2['event_time']=df2['message'].str.replace('\(\d{1,2}\.\d{1,2}\)\s+о\s+', '', regex=True) #gat time
        df2['start_event']=df2['event_date']+' '+ df2['event_time']
        #df2['start_event'] = df2["start_event"].apply(lambda x: datetime.strptime(x, '%d.%m.%Y %H:%M').isoformat())
        df2['start_event'] = df2["start_event"].apply(lambda x: datetime.strptime(x, '%d.%m.%Y %H:%M')) #change to datatime
        #df2= df2[df2['start_event'] >= pd.to_datetime('today')] 
        df2['end_event'] = df2["start_event"].apply(lambda x: x + timedelta(hours=1)) #add 1 hours 

        current_dateTime = pd.to_datetime('today')
        df_upcoming= df2[df2['start_event'] >= current_dateTime].copy()

        df_upcoming['start_event'] = df_upcoming["start_event"].apply(lambda x: (x.tz_localize('Europe/Kyiv')).isoformat()) #change to isoformat
        df_upcoming['end_event'] = df_upcoming["end_event"].apply(lambda x: (x.tz_localize('Europe/Kyiv')).isoformat())    
        df_upcoming['location']='Ukraine'
        df_upcoming=df_upcoming[['event_name', 'description',  'start_event', 'end_event', 'location']]
    else:
        df_upcoming = pd.DataFrame(columns=['event_name', 'description', 'start_event','end_event','location'])
    return df_upcoming


#df0=get_date(events_name)
#df_upcoming=filter_nice(df0)

