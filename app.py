import configparser
import time

from telethon import functions
from telethon.sync import TelegramClient 
from datetime import datetime, timezone, timedelta 

# reading Telegram credentials
config = configparser.ConfigParser() 
 
#Your Telegram login details
api_id = 123456789
api_hash = 'aasssddd123456789'
username = 'Nikita' 

version = '0.1'

print('PyBot v' + version) 
print('Starting..') 

client = TelegramClient(username, api_id, api_hash)
client.start()   

def Start(username, api_id, api_hash, peer, time_start, message, time_sleep):

    if not api_id:
        print('Error! Not app_id.')
    elif not api_hash:
        print('Error! Not api_hash.')
    elif not username:
        print('Error! Not username.')
    else: 
        print('Connecting to Telegram..')
    if not peer:
        peer = input('Enter username or chat_id:\n') 
    if not message:
        message = str(input('Enter the text of the message:\n'))
    
    sum_time = int(input('Specify the period between messages (in minutes):\n'))
    if not sum_time:
        print('Error! Invalid value')

    # we get the date of the last scheduled message in the specified chat
    def GetScheduledHistoryRequest(peer): 
        result = client(functions.messages.GetScheduledHistoryRequest(
            peer=peer,
            hash=0
        ))  
        return result
    
    get_history = GetScheduledHistoryRequest(peer)
    
    if len(get_history.messages) != 0:
        date = get_history.messages[0].date  

        if time.mktime(date.timetuple()) > time.mktime(time_start.timetuple()): # if the previously specified time is less than the last one, then select the last one
            time_start = get_history.messages[0].date

    limit = len(get_history.messages)
    limit = 100 - limit # as of May 2022, you cannot publish scheduled messages in the amount of more than 100
 
    print(' Chat: ' + str(peer) 
    + '\n Message: ' + str(message) 
    + '\n Date of the last scheduled message: ' + str(time_start)
    + '\n Remaining limit:' + str(limit))

    print('Starting work!')
    
    i = 0
    while i < limit:
        i += 1
        time_start = time_start + timedelta(minutes=sum_time) # the period between each subsequent message

        time.sleep(time_sleep) # пауза
        print('+ Scheduled message added \'' + str(message) + '\' in the \'' + str(peer) + ' dialog \' time: ' + str(time_start))
        
        result = client(functions.messages.SendMessageRequest(
            peer=peer,  
            schedule_date=time_start,
            message=message
        )) 
        if result.updates[0].id > 0:
            print('Done! message id: ' + str(result.updates[0].id) + ' Left: ' + str(limit - i))
            
    print('Done!') 

# You can specify your default data
time_sleep = 0.5 # pause in the loop
peer = 'durov'
message = 'Test messages'
time_start = datetime(2022, 12, 31, 0, 00, 00) # publication start time (format: year, month, day, hours, minutes, seconds)
  
if not time_start:
    time_start = datetime.now(timezone.utc) 

Start(username, api_id, api_hash, peer, time_start, message, time_sleep) 
