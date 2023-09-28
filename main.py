#!/usr/bin/env python
# coding: utf-8



import os.path
import import_ipynb
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pandas as pd
from datetime import datetime, timedelta

from telegram_parser import telegram_function
import pprint




SCOPES = ['https://www.googleapis.com/auth/calendar']
calendar_id='9bc14bd466babbb554a9f82e96267588e47bfad8783d9548cfb05b1fdc853343@group.calendar.google.com'


#---------------------------------------------------------------------------------

print('\n\nAll possible event organizers:\n')
dict_event=[
#site
{'event_name': 'Speakday', 'description':'https://speakday.com/timetable/english-conversations'},
{'event_name': 'Langclub', 'description':'https://langclub.live/sessions'},
#telegram
{'event_name': 'Nice', 'description':'https://t.me/speaking_club_nice'},
{'event_name': 'English Bro', 'description':'https://t.me/your_english_bro'},
{'event_name': 'Small Talks', 'description':'https://t.me/smalltalksproject'},
#regulat meating
{'event_name': 'Buki', 'description':'https://t.me/speaking_club_easyschool'},
{'event_name': 'Green Forest', 'description':'https://t.me/english_events'},
#telegram head input
{'event_name': 'Might of Speech', 'description':'https://t.me/mightofspeech'},
]
for (i, item) in enumerate(dict_event):
    #print(i, item['event_name'], '\t\t\tsite', item['description'])
    line_new = '%2s  %20s  %20s' % (i, item['event_name'], item['description'])
    print (line_new)

print ('\n')


  



#chanel_list=['https://t.me/smalltalksproject',  'https://t.me/speaking_club_nice', 'https://t.me/your_english_bro']
#chanel_list







#---------------------------------------------------------------------------------


'''
MightofSpeech
'''
#manual
def MightofSpeech():
    from MightofSpeech import  get_mightofspeech
    df_get=get_mightofspeech()
    return df_get


#---------------------------------------------------------------------------------


'''
Telegram Function 
'''

#telegram_function()
#return file with data


'''
Get data from file creating by Telegram Function
'''

def get_date_tg_file(events_name):
    
    save_file_path='chanel_messages.json'

    f = open(save_file_path)
    import_data = json.load(f)
    #if len(import_data)==0:
    #    print('Don\'t have any data')
    #else: print('\nFile %s get %s rows \n' % (save_file_path, len(import_data)))




    data = pd.DataFrame(import_data)
    event= pd.DataFrame(dict_event)

    merged_df = pd.merge(data, event)
    #print(merged_df.to_dict('records'))
    if events_name!='':
        df=merged_df[merged_df['event_name']==events_name].copy()
    else: df=merged_df
    return df

#get_date_tg_file(events_name)



#---------------------------------------------------------------------------------

'''
Nice - index 2
'''
def Nice():
    from Nice import  filter_nice
    df0=get_date_tg_file('Nice')
    df_get=filter_nice(df0)
    df_get=df_get[df_get['event_name']=='Nice'].copy()
    print('Chanel "Nice" have %s upcoming event' % (len(df_get)))
    
    return df_get


'''
Bro - index 3
'''
def Bro():
    from Bro import  filter_bro
    df0=get_date_tg_file('English Bro')
    df_get=filter_bro(df0)
    df_get=df_get[df_get['event_name']=='English Bro'].copy()
    print('Chanel "English Bro" have %s upcoming event' % (len(df_get)))
    return df_get


'''
SmallTalks - index 4
'''
def SmallTalks():
    from SmallTalks import   filter_smalltalks
    df0=get_date_tg_file('Small Talks')
    df_get=filter_smalltalks(df0)
    df_get=df_get[df_get['event_name']=='Small Talks'].copy()
    print('Chanel "Small Talks" have %s upcoming event' % (len(df_get)))
    return df_get


#---------------------------------------------------------------------------------


def Langclub():
    from Langclub import  get_page, filter_langclub
    url='https://langclub.live/sessions'
    bs_langclub=get_page(url) 
    df_get=filter_langclub(bs_langclub)
    return df_get

def Speakday():
    from Speakday import  get_page, filter_speakday
    url='https://speakday.com/timetable/english-conversations'
    bs_speakday=get_page(url) 
    df_get=filter_speakday(bs_speakday)
    return df_get


'''
Get existing events
'''

def get_evet_calendar(events_name):
    list_exist_event=[]
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credential_calendar_python.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('calendar', 'v3', credentials=creds)
        
        # https://developers.google.com/calendar/api/guides/create-events#python_1
        # https://developers.google.com/calendar/quickstart/python
        # https://developers.google.com/calendar/api/v3/reference/events/list
        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('\nGetting the upcoming %s events' %events_name)
        events_result = service.events().list(calendarId=calendar_id, timeMin=now,
                                              q=events_name, #text search by summary, description, email etc
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('\nNo upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))           
            print(start, event['summary'])
            list_exist_event.append({'event_name': event['summary'],'start_event': start}) 


    except HttpError as error:
        print('\nAn error occurred: %s' % error)
    return list_exist_event

#---------------------------------------------------------------------------------

'''
Show which event exist 
'''


        
def show_event():        
    list_exist_event=[]
    possible_answers=[str(i) for i in range(0,len(dict_event))]+['tg'] +['site']+ ['']+ ['all'] 
    print('\npossible answers:', ['number(0-%s)' % len(dict_event)]+possible_answers[len(dict_event):])

    answer = None
    while answer not in possible_answers: 
        answer = input('Select organization number: ') 
        if answer == 'all' or answer =='':  #print all upcoming event (limit =10)
            events_name=''
            list_exist_event=get_evet_calendar(events_name)

        elif answer =='tg':   #print only for tg
            events_name='/t.me/'
            list_exist_event=get_evet_calendar(events_name)
            #print('list_exist_event', list_exist_event)
            events_name='tg'

        elif answer =='site':   #print only for tg
            events_name='Speakday'
            list_exist_event_speak=get_evet_calendar(events_name)
            events_name='Langclub'
            list_exist_event_lang=get_evet_calendar(events_name)
            list_exist_event=list_exist_event_speak+list_exist_event_lang
            events_name='site'



        elif answer in possible_answers[:len(dict_event)]:   #print only event of some organization
            events_id=int(answer)
            events_name=dict_event[int(events_id)]['event_name']
            list_exist_event=get_evet_calendar(events_name)
            #print('list_exist_event', list_exist_event)

        else: 
            print('Error! Please enter (1-7) or "all"') 



    df_exist_event=pd.DataFrame(data=list_exist_event)
    return df_exist_event, events_name

#-----manual selection   
answer_exist = None 
while answer_exist not in ("y", "n"): 
    answer_exist = input("Do you want to see existing events? Enter (y/n): ") 
    if answer_exist == "y": 
        df_exist_event, events_name=show_event()
    elif answer_exist == "n": 
        print('Don\'t want')
        events_name=''
    else: 
        print("Please enter y or n.") 


#events_id=input('Select organization number, for all press ENTER:')
#event_name=dict_event[int(events_id)]['event_name']


#---------------------------------------------------------------------------------

'''
Get new event 
'''



def case_event(event_name):
    print('')
    match event_name:



        case 'Speakday':
            return Speakday()
        case 'Langclub':
            return Langclub()

        case 'site': 
            return pd.concat([Speakday(), Langclub()])

        case 'Nice':
            telegram_function(events_name)
            return Nice()
        case 'English Bro':
            telegram_function(events_name)
            return Bro()
        case 'Small Talks':
            telegram_function(events_name)
            return SmallTalks()

        case 'tg': 
            telegram_function('')
            df=pd.concat([Nice(), Bro(), SmallTalks()])
            return df

        case 'Might of Speech': 

            return MightofSpeech()

        case '':
            telegram_function('')
            df=pd.concat([Nice(), Bro(), SmallTalks(), Speakday(), Langclub()])
            return df
        case _:
            return "Something's wrong with the internet"


#---------------------------------------------------------------------------------


'''
Insert new event 
'''


def insert_event(df_new_event):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credential_calendar_python.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('calendar', 'v3', credentials=creds)
        
        # https://developers.google.com/calendar/api/guides/create-events#python_1
        # https://developers.google.com/calendar/quickstart/python
        for i in range(0,len(df_new_event)):
            event = {
              'summary': df_new_event['event_name'][i],
              'location': df_new_event['location'][i],
              'description': df_new_event['description'][i],
              'colorID':'2',
              'start': {
                'dateTime': df_new_event['start_event'][i],
                'timeZone': 'Europe/Kyiv',
                       },
              'end':   {
                'dateTime': df_new_event['end_event'][i],
                'timeZone': 'Europe/Kyiv',
                        }
                    }

            event = service.events().insert(calendarId=calendar_id, body=event).execute()
            print ('Event at %s created: %s' % (df_new_event['start_event'][i], event.get('htmlLink')))

    except HttpError as error:
        print('An error occurred: %s' % error)


#---------------------------------------------------------------------------------

'''
Selection 
'''

answer_upcomin = None 
while answer_upcomin not in ("y", "n"): 
    answer_upcomin = input("\nDo you want looking for new events? Enter (y/n): ") 
    if answer_upcomin == "y": 
        print('\n...function take data runing...')
        print('case_event', events_name)
        df_upcoming=case_event(events_name)  #get all event
        print('\nUpcoming events:', len(df_upcoming))
        if len(df_upcoming)>0:
            try:
                if len(df_exist_event)==0: df_exist_event = pd.DataFrame(columns=['event_name', 'start_event']) 
            except Exception:
                print('We did\'nt check for existing events')
                df_exist_event = pd.DataFrame(columns=['event_name', 'start_event']) 

            #filter new events to already existing events 
            df_new_event=pd.merge(df_upcoming[df_upcoming.columns.tolist()],
                                  df_exist_event[["event_name", "start_event"]],
                                  indicator=True, how='outer')\
                                  .query('_merge=="left_only"').drop('_merge', axis=1)\
                                  .reset_index(drop=True)
            print('Of them %s event is new' % len(df_new_event))
            pprint.pprint(df_new_event[['event_name', 'start_event']].to_dict('records'))

            #-----manual selection
            if len(df_new_event)>0:
                answer_insert = None 
                while answer_insert not in ("y", "n"): 
                    answer_insert = input("\nDo you want insert data? Enter (y/n): ") 
                    if answer_insert == "y": 
                        print('\n...function insert runing...')
                        insert_event(df_new_event)
                    elif answer_insert == "n": 
                        print('Don\'t want')
                    else: 
                        print("Please enter y or n") 
            else:
                print('We don\'t insert data, because there are no new events')
        else:
            print('We don\'t insert data, because there are no upcoming events')

    elif answer_upcomin == "n": 
        print('Don\'t want')
    else: 
        print("Please enter y or n") 


print('\n')




