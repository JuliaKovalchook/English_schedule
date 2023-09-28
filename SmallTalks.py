#!/usr/bin/env python
# coding: utf-8



import json
import re
import regex
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
        elif row["description"] == "https://t.me/smalltalksproject":
            return "Small Talks"    

        else:
            return "speaking club"

    df = df.assign(event_name=df.apply(set_event, axis=1))
    df0=df[df['event_name']=='Small Talks'].copy()
    return df0

def filter_smalltalks(df0):
    #find  only the channel Small Talks

    '''
    Filter all message by pattern 

    pattern looks like #Цього четвергу о 19:00
    looking for "(16.09) о 12:00"  
    '''
    if len(df0)>0:
        day_of_week_ukr=['понеділ', 'вівіторок', 'серед', 'четвер', 'субот', 'неділ']  #possible options for writing the day of the week
        pattern= r"\L<words>[а-я]*.*\d:\d{2}" 

        df0['message'] = df0['message'].apply(lambda x:  regex.findall(pattern, x, words=day_of_week_ukr))  #get {week_name}&{trash}&{time_event}
        df0=df0.explode('message') #if one message has several events, we separate them 
        df0.dropna(subset=['message'], inplace=True) #drop all rows wo information about event 
        df0['name_week'] = df0['message'].apply(lambda x:  regex.findall(r"\L<words>", x, words=day_of_week_ukr)[0]) #get short {week_name} from list 
        df0=df0.reset_index(drop=True) 


        df0['number_week']=df0['name_week'].apply(lambda x: day_of_week_ukr.index(x)) #get number of week
        df0['start_week']=df0['date'].apply(lambda x: (datetime.strptime(x.split(' ')[0], "%Y-%m-%d")) - timedelta(days=\
                                                       (datetime.strptime(x.split(' ')[0], "%Y-%m-%d")).weekday())) #start of week by date of post


        df0['start_event_date'] = df0[['start_week','number_week' ]]\
                                 .apply(lambda x:x['start_week'] + timedelta(days=x['number_week']), axis=1) # {date of post}+{number_week}
        df0['time_event'] = df0['message'].apply(lambda x:  regex.findall(r"\d{2}:\d{2}", x)[0])
        df0['start_event']=df0[['start_event_date','time_event' ]]\
                                 .apply(lambda x:x['start_event_date'] + timedelta(
                                            hours=int(x['time_event'].split(':')[0]),
                                            minutes=int(x['time_event'].split(':')[1])), axis=1) #start_event with date and time
        df0['end_event'] = df0["start_event"].apply(lambda x: x + timedelta(hours=1)) #add 1 hours 

        current_dateTime = pd.to_datetime('today')

        df_upcoming= df0[df0['start_event'] >= current_dateTime].copy()
        
        df_upcoming['start_event'] = df_upcoming["start_event"].apply(lambda x: (x.tz_localize('Europe/Kyiv')).isoformat()) #change to isoformat
        df_upcoming['end_event'] = df_upcoming["end_event"].apply(lambda x: (x.tz_localize('Europe/Kyiv')).isoformat())
        df_upcoming['location']='Ukraine'
        df_upcoming=df_upcoming[['event_name', 'description',  'start_event', 'end_event', 'location']]
    else:
        df_upcoming = pd.DataFrame(columns=['event_name', 'description', 'start_event','end_event','location'])
    return df_upcoming

#df0=get_date()
#df_upcoming=filter_smalltalks(df0)
#print(df_upcoming)
