from groq import Groq
import os
from dotenv import load_dotenv
from app.services.youtube_service import get_youtube_recommendations

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
try:
    client = Groq(api_key=GROQ_API_KEY, http_client=None)
except Exception as e:
    print(f"Groq Client Initialization Error: {e}")

def get_chatbot_response(query):
    try:
        prompt = f"Answer this fitness question concisely: {query}"
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            max_tokens=150
        )
        text_response = response.choices[0].message.content.strip()

        youtube_query = f"gym {query}"
        videos = get_youtube_recommendations(youtube_query)
        if videos:
            video = videos[0]
            video_link = f"https://youtu.be/{video['video_id']}"
            return f"{text_response}\n\nWatch this video: {video_link}"
        return text_response
    except Exception as e:
        print(f"Chatbot Error: {e}")
        return "Sorry, I couldn't process your request. Please try again later."