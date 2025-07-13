from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji
import pandas as pd
from textblob import TextBlob
def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
       
    num_messaages = df.shape[0]
    #fetch number of words
    words = []
    for message in df['message']:
        words.extend(message.split())
    
    #fetch number of media
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    
    #etch number of links
    extractor = URLExtract()
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    
    return num_messaages, len(words),num_media_messages, len(links)

def most_busy_users(df):
    x = df['users'].value_counts().head()
    per = round(df['users'].value_counts()/ df.shape[0] * 100,2).reset_index().rename(columns={'users': 'name', 'counts': 'percentage'})
    return x, per

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    temp = df[df['message'] != '<Media omitted>\n']
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp = wc.generate(' '.join(temp['message']))
    
    return temp

#emoji analysis 
def emoji_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=['Emoji', 'Count'])
    return emoji_df

# Time analysis
def time_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    df['month_num'] = df['message_date'].dt.month
    timeline = df.groupby(['Year', 'month_num', 'Month']).count()['message'].reset_index()
    time = []
    
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))
    timeline['time'] = time
    
    return timeline

def most_active_days(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    day_activity = df['message_date'].dt.day_name().value_counts()
    return day_activity
