# 💪 Gym Video Recommender

**Yo bro, welcome to the Gym Video Recommender!**

This Streamlit app hooks you up with dope YouTube workout videos, answers fitness questions with a smart chatbot, and tracks your daily exercises with slick charts and stats. Whether you're a gym rat or just starting out, it's your go-to fitness buddy.

---

## 🚀 Features

### 🧠 Fitness Helper Chatbot
- Ask fitness questions like:  
  `"muscle gain"` or `"fat loss"` or `"best cardio"`.
- Get advice powered by **Groq's llama-3.3-70b-versatile** model.
- Includes a relevant YouTube video link.

---

### 🏋️ Daily Exercise Plan
- Auto-suggested exercises based on your query (e.g., `"muscle gain"` → Bench Press, Squats).
- Tick checkboxes to log workouts (15 min each).
- ✅ Hit `Log Exercise` to add to today's log.
- 💾 Use `Save Logs` to save to `exercise_log.csv`.

---

### 📊 Visual Stats
- **Bar Chart** – Daily workout minutes over the last 7 days.
- **Pie Chart** – Breakdown of how often you hit each exercise.
- **Progress Stats:**
  - Weekly minutes (goal: 150 min)
  - Minutes left
  - Daily target
  - Workout consistency %

---

### 🔍 Smart Workout Search
- Search workouts (e.g., `"HIIT"`, `"yoga"`) via YouTube.
- Apply filters:
  - Duration: Short / Medium / Long
  - Type: Strength, Cardio, Yoga
  - Difficulty: Beginner, Intermediate, Advanced
- Watch embedded videos with summaries and tags.
- 📥 Download recommendations as CSV.

---

### 💅 Clean & Styled UI
- Styled with `styles.css`
- Custom green buttons (`#28a745`) for logging/saving
- Mobile-friendly layout

---

## 🗂️ Project Structure

gym_video_recommender/
├── .gitignore
├── .env
├── README.md
├── requirements.txt
├── main.py
└── app/
    ├── __init__.py
    ├── services/
    │   ├── youtube_service.py
    │   ├── groq_service.py
    │   ├── recommender.py
    |   |── suggestions.py
    │   ├── chatbot.py
    │   └── __init__.py
    ├── core/
    │   ├── config.py
    │   ├── utils.py
    │   └── __init__.py
    |
    ├── static/
    │   ├── css/
    │   │   └── styles.css
    │   └── __init__.py
    ├── models/
    │   ├── schema.py
    │   └── __init__.py