from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def get_youtube_recommendations(search_query):
    try:
        search_response = youtube.search().list(
            q=search_query,
            part='snippet',
            type='video',
            maxResults=10,
            relevanceLanguage='en',
            safeSearch='moderate'
        ).execute()

        recommendations = []
        for item in search_response.get('items', []):
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            if len(video_id) == 11:
                recommendations.append({
                    'title': title,
                    'video_id': video_id,
                    'summary': None,
                    'tags': []
                })
        return recommendations
    except:
        return []