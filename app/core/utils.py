import pandas as pd
import io

def get_suggestions():
    return [
        "beginner workout",
        "abs workout",
        "weightlifting",
        "cardio",
        "HIIT",
        "yoga",
        "strength training",
        "bodyweight exercises",
        "dumbbell workout",
        "stretching"
    ]

def save_to_csv(data):
    df = pd.DataFrame(data)
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue()