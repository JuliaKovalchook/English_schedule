#!/usr/bin/env python
# coding: utf-8

# In[3]:


from datetime import datetime, timedelta
import pandas as pd



# In[6]:

def test_mig():
    x='xxx'
    return x  

def get_mightofspeech():
    list_event=[]

    while True:
        day_of_event=input('Press day of event from 1 to 7 or end : ')
        if day_of_event=='end':
            break
        else:
            time_of_event=input('Press time of event (like 16): ')
            day_of_event=int(day_of_event)
            dt=datetime.today()
            start_week = dt - timedelta(days=dt.weekday())
            start_date = (start_week + timedelta(days=int(day_of_event)-1)).date()
            start_time = datetime.strptime(time_of_event, '%H').time()
            start_event=datetime.strptime(str(start_date)+' '+ str(start_time), '%Y-%m-%d %H:%M:%S')
            end_event=start_event+ timedelta(hours=1)

            print('Add event %s on %s' % (str(start_event), start_event.strftime("%A")))
            #print(end_event)
            start_event=start_event.isoformat()
            end_event=end_event.isoformat()

            event_name='Might of Speech'
            url='https://t.me/mightofspeech'
            location='Ukraine'
            my_information = {'event_name': event_name, 
                              'description':url,
                              'location': location,
                              'start_event': start_event,
                              'end_event': end_event
                             }

            list_event.append(my_information)
    if len(list_event)>0:
        df_upcoming = pd.DataFrame(data=list_event)
    else:
        df_upcoming = pd.DataFrame(columns=['event_name', 'description', 'start_event','end_event','location'])        
    return df_upcoming
        

