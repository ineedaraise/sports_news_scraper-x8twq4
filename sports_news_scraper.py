import requests
from bs4 import BeautifulSoup
import pandas as pd
from googleapiclient.discovery import build

def scrape_mlb_news(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    articles = soup.find_all('article', class_='article')
    
    news_data = []
    for article in articles:
        title = article.find('h2', class_='article-title').text.strip()
        summary = article.find('p', class_='article-summary').text.strip()
        date = article.find('span', class_='article-date').text.strip()
        
        news_data.append({
            'Title': title,
            'Summary': summary,
            'Date': date
        })
    
    return pd.DataFrame(news_data)

def scrape_youtube_channel(channel_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    request = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        type='video',
        order='date',
        maxResults=50
    )
    
    response = request.execute()
    
    videos_data = []
    for item in response['items']:
        video_data = {
            'Title': item['snippet']['title'],
            'Description': item['snippet']['description'],
            'Published At': item['snippet']['publishedAt'],
            'Video ID': item['id']['videoId']
        }
        videos_data.append(video_data)
    
    return pd.DataFrame(videos_data)

def main():
    mlb_url = 'https://www.mlb.com/yankees/news'
    mlb_news_df = scrape_mlb_news(mlb_url)
    print("MLB News:")
    print(mlb_news_df)
    
    youtube_api_key = 'YOUR_YOUTUBE_API_KEY'
    mlb_channel_id = 'UCoLrcjPV5PbUrUyXq5mjc_A'  # MLB YouTube channel ID
    youtube_videos_df = scrape_youtube_channel(mlb_channel_id, youtube_api_key)
    print("\nYouTube Videos:")
    print(youtube_videos_df)

if __name__ == '__main__':
    main()