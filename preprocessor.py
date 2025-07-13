import re
import pandas as pd
def preprocess(data):
    #this below is for patter recognication and extract the according to it. from re(regular expression)
    # 
    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\u202f(?:am|pm)\s-\s" #can check in regx.com 
#above line meaning,\d (can be digit) consisting of {1 OR 2} Length (Day) / \d(can be digit) of lenth 1 or 2 (MONTH)and again a digit \d consisting {2 or 4 length YEAR}
    message = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)
    df = pd.DataFrame({'user_message':message, 'message_date':dates})
    df['message_date'] = df['message_date'].str.replace('\u202f', ' ', regex=False)
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p - ')
    
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s',message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['users'] = users
    df['message'] = messages
    df.drop(columns= ['user_message'], inplace = True)
    
    df = df[~df['message'].isin([
        "This message was deleted\n",
        "Messages and calls are end-to-end encrypted. Only people in this chat can read, listen to, or share them. Learn more.\n",
    ])]
    
    
    df['Year'] = df['message_date'].dt.year
    df['Month'] = df['message_date'].dt.month_name()
    df['Day'] = df['message_date'].dt.day
    df['Hour'] = df['message_date'].dt.hour
    df['Minute'] = df['message_date'].dt.minute
    return df