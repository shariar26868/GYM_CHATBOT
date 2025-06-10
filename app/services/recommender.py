from app.services.groq_service import generate_summary, generate_tags
from app.models.schema import Recommendation, Tag
from app.core.config import DURATION_RANGES

def apply_recommendation_filters(recommendations, duration, workout_type, difficulty, preferences):
    filtered = []
    for rec in recommendations:
        if not rec.get('summary'):
            rec['summary'] = generate_summary(rec['title'])
        if not rec.get('tags'):
            rec['tags'] = generate_tags(rec['title'])

        keep = True
        title_lower = rec['title'].lower()
       
        if workout_type != "Any" and workout_type.lower() not in title_lower:
            keep = False
        if difficulty != "Any" and difficulty.lower() not in title_lower:
            keep = False
        if preferences.get("goal") and preferences["goal"].lower() not in title_lower:
            keep = keep and False  
        if preferences.get("equipment") and preferences["equipment"].lower() not in title_lower:
            keep = keep and False 

        if keep:
            rec['tags'] = [Tag(label=tag.label, confidence=tag.confidence) for tag in rec['tags']]
            filtered.append(Recommendation(**rec))

    return filtered[:5]