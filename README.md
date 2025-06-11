# 💪 Gym Video Recommender

**Yo bro, welcome to the Gym Video Recommender!**

This Streamlit app hooks you up with dope YouTube workout videos, answers fitness questions with a smart chatbot, and tracks your daily exercises with slick charts and stats. Whether you're a gym rat or just starting out, it's your go-to fitness buddy.

---

![Workout UI](https://github.com/user-attachments/assets/dffd35d4-4c55-4321-b83c-dc989f35b0b7)
![Charts UI](https://github.com/user-attachments/assets/0db0ab7f-2408-4825-b5c9-01d900407d80)

## 🚀 Features

### 🧠 Fitness Helper Chatbot
- Ask fitness questions like:  
  `"muscle gain"`, `"fat loss"`, `"best cardio"`
- Get real-time fitness advice powered by **Groq's LLaMA 3.3 70B Versatile** model
- Includes a relevant YouTube video link for your query

### 🏋️ Daily Exercise Plan
- Auto-suggests exercises based on goals (e.g., `"muscle gain"` → Bench Press, Squats)
- Tick checkboxes to log 15-minute workout sessions
- ✅ Click `Log Exercise` to add to today’s log
- 💾 Hit `Save Logs` to save to `exercise_log.csv`

### 📊 Visual Stats Dashboard
- **Bar Chart** – Tracks daily workout minutes over the last 7 days
- **Pie Chart** – Shows frequency of exercises performed
- **Progress Overview**:
  - Weekly workout goal (150 min)
  - Minutes left to goal
  - Suggested daily target
  - Workout consistency %

### 🔍 Smart Workout Search
- Search YouTube for workouts like `"HIIT"`, `"yoga"`, etc.
- Use filters:
  - Duration: Short / Medium / Long
  - Type: Strength, Cardio, Yoga
  - Difficulty: Beginner / Intermediate / Advanced
- Watch embedded videos with auto-generated summaries and tags
- 📥 Export recommendations to CSV

### 💅 Modern UI & UX
- Styled with custom CSS (`styles.css`)
- Green custom buttons: `#28a745` for logging/saving actions
- Mobile-responsive layout for on-the-go users

---

## 🗂️ Project Structure
```
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
    │   ├── suggestions.py
    │   ├── chatbot.py
    │   └── __init__.py
    ├── core/
    │   ├── config.py
    │   ├── utils.py
    │   └── __init__.py
    ├── static/
    │   ├── css/
    │   │   └── styles.css
    │   └── __init__.py
    ├── models/
    │   ├── schema.py
    │   └── __init__.py
```

---

## 📌 To-Do / Improvements
- [ ] Add user authentication
- [ ] Dark mode toggle
- [ ] Personalized progress recommendations
- [ ] Voice-enabled chatbot
- [ ] Workout calendar with reminders

---

## 📦 Installation
```bash
git clone https://github.com/your-username/gym_video_recommender.git
cd gym_video_recommender
pip install -r requirements.txt
streamlit run main.py
```

---

## 🧠 Powered By
- [Streamlit](https://streamlit.io/)
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [Groq LLaMA 3.3-70B](https://groq.com/)

---

Made with ❤️ by [Md.Shariar Emon Shaikat]

