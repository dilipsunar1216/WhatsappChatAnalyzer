import streamlit as st
import helper
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
import emoji
import pandas as pd
from textblob import TextBlob
import seaborn as sns
import preprocessor

# Page configuration
st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")

# Optional CSS for styling
st.markdown("""
    <style>
    h1, h2, h3 {
        color: #2E3B4E;
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton>button {
        color: white;
        background: linear-gradient(90deg, #1d976c, #93f9b9);
        border-radius: 8px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("## 📊 WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("📁 Upload a WhatsApp chat file")
if uploaded_file is not None:
    byte_data = uploaded_file.getvalue()
    data = byte_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.markdown("### 🧾 Chat Preview")
    st.dataframe(df, use_container_width=True)

    user_list = df['users'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox("👤 Show analysis with respect to", user_list)
    if st.sidebar.button("🔍 Show Analysis"):
        num_messages, num_words, num_media_message, links_num = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(label="💬 Total Messages", value=num_messages)
        with col2:
            st.metric(label="📝 Total Words", value=num_words)
        with col3:
            st.metric(label="🖼️ Media Messages", value=num_media_message)
        with col4:
            st.metric(label="🔗 Total Links Shared", value=links_num)

        # Time Analysis
        st.markdown("### ⏰ Monthly Message Timeline")
        time = helper.time_analysis(selected_user, df)
        fig = px.line(time, x='time', y='message', markers=True,
                      title='Monthly Message Volume',
                      labels={'time': 'Month-Year', 'message': 'Message Count'},
                      template='plotly_white')
        fig.update_traces(line_color='#067FE9', line_width=3)
        st.plotly_chart(fig, use_container_width=True)

        # Most Busy Users
        if selected_user == 'Overall':
            st.markdown("### 🧑‍🧛‍🧑 Top Active Users")
            x, percentage_df = helper.most_busy_users(df)
            fig = px.bar(x, x=x.index, y=x.values, labels={'x': 'User', 'y': 'Messages'},
                         color_discrete_sequence=["#067FE9"], text_auto=True, title='Top 5 Active Users')
            fig.update_layout(xaxis_tickangle=-45, template='plotly_white')
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                st.dataframe(percentage_df, use_container_width=True)

        # Word Cloud
        st.markdown("### ☁️ Word Cloud")
        df_wordcloud = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wordcloud)
        plt.axis('off')
        st.pyplot(fig)

        # Emoji Analysis
        st.markdown("### 😄 Emoji Analysis")
        emojis = helper.emoji_analysis(selected_user, df)
        st.dataframe(emojis)

        # Most Active Days
        st.markdown("### 📅 Most Active Days")
        active_days = helper.most_active_days(selected_user, df)
        fig = px.bar(x=active_days.index, y=active_days.values,
                     labels={'x': 'Day', 'y': 'Messages'},
                     color_discrete_sequence=['#067FE9'],
                     title='Messages by Day of the Week')
        fig.update_layout(xaxis_title='Day', yaxis_title='Messages', template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
