# WhatsApp Chat Analyzer (Basic Version)

This is a Streamlit-based app that analyzes a WhatsApp group or personal chat export. It displays key statistics, timelines, word clouds, emoji usage, and user activity levels.

## 💻 Features

- Upload a `.txt` file of WhatsApp chat exports
- Basic message stats:
  - Total messages
  - Word count
  - Media messages
  - Shared links
- Time-based message trends
- WordCloud of most frequent terms
- Emoji usage frequency
- Most busy users in the chat

## 📦 Requirements

- Python 3.8+
- Libraries:
  - streamlit
  - pandas
  - matplotlib
  - wordcloud
  - emoji
  - urlextract

Install using:

```bash
pip install -r requirements.txt
