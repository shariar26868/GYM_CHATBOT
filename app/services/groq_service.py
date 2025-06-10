from groq import Groq
import os
from dotenv import load_dotenv
from app.models.schema import Tag

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def generate_summary(title):
    try:
        prompt = f"Summarize gym video title in 1-2 sentences: {title}"
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="mixtral-8x7b-32768"
        )
        return response.choices[0].message.content.strip()
    except:
        return "Summary not available."

def generate_tags(title):
    try:
        prompt = f"Generate 3-5 tags for gym video '{title}' with confidence (Low, Medium, High)."
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="mixtral-8x7b-32768"
        )
        tags_text = response.choices[0].message.content.strip()
        tags = []
        for line in tags_text.split("\n"):
            if line.strip():
                label, confidence = line.rsplit(" (", 1) if "(" in line else (line, "Medium")
                tags.append(Tag(label=label.strip(), confidence=confidence.rstrip(")")))
        return tags[:5]
    except:
        return [Tag(label="General Workout", confidence="Medium")]