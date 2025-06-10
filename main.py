import streamlit as st
import pandas as pd
import datetime
import json
from app.services.youtube_service import get_youtube_recommendations
from app.services.recommender import apply_recommendation_filters
from app.services.chatbot import get_chatbot_response
from app.core.config import DURATION_RANGES, WORKOUT_TYPES, DIFFICULTY_LEVELS
from app.services.suggestions import get_suggestions

st.set_page_config(page_title="Gym Video Recommender", layout="wide")
with open("app/static/css/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.markdown("""
    <style>
    .stButton > button {
        background-color: #28a745 !important;
        color: white !important;
        border: none !important;
        padding: 10px 20px !important;
        border-radius: 5px !important;
        font-weight: bold !important;
    }
    .stButton > button:hover {
        background-color: #218838 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

def save_to_csv(data):
    df = pd.DataFrame(data)
    return df.to_csv(index=False).encode('utf-8')

def initialize_session_state():
    if 'exercise_log' not in st.session_state:
        st.session_state.exercise_log = {}  
    if 'last_updated' not in st.session_state:
        st.session_state.last_updated = datetime.date.today()
    if 'last_query' not in st.session_state:
        st.session_state.last_query = ""
    if 'recommended_exercises' not in st.session_state:
        st.session_state.recommended_exercises = []

def log_exercise(exercises):
    today = datetime.date.today()
    if today not in st.session_state.exercise_log:
        st.session_state.exercise_log[today] = {}
    durations = {ex: 15 for ex in st.session_state.recommended_exercises}  
    for exercise, completed in exercises.items():
        st.session_state.exercise_log[today][exercise] = durations[exercise] if completed else 0
    st.session_state.last_updated = today

def get_progress_data():
    today = datetime.date.today()
    days = [(today - datetime.timedelta(days=i)) for i in range(6, -1, -1)]
    data = {"Date": [], "Minutes": []}
    for day in days:
        total = sum(st.session_state.exercise_log.get(day, {}).values())
        data["Date"].append(day.strftime("%Y-%m-%d"))
        data["Minutes"].append(total)
    return pd.DataFrame(data)

def get_exercise_distribution():
    exercise_counts = {}
    for day, exercises in st.session_state.exercise_log.items():
        for exercise, minutes in exercises.items():
            if minutes > 0:
                exercise_counts[exercise] = exercise_counts.get(exercise, 0) + 1
    return pd.DataFrame({
        "Exercise": list(exercise_counts.keys()),
        "Days Completed": list(exercise_counts.values())
    })

def predict_progress():
    weekly_goal = 150  
    today = datetime.date.today()
    week_start = today - datetime.timedelta(days=today.weekday())
    weekly_total = 0
    for i in range(7):
        day = week_start + datetime.timedelta(days=i)
        weekly_total += sum(st.session_state.exercise_log.get(day, {}).values())
    days_left = 6 - today.weekday() if today.weekday() < 6 else 0
    remaining = max(0, weekly_goal - weekly_total)
    daily_needed = remaining / (days_left + 1) if days_left >= 0 else remaining
    return weekly_total, remaining, daily_needed

def render_chart(chart_config, chart_id, height=400):
    html = f"""
    <div>
        <canvas id="{chart_id}"></canvas>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        const ctx = document.getElementById('{chart_id}').getContext('2d');
        new Chart(ctx, {json.dumps(chart_config)});
    </script>
    """
    st.components.v1.html(html, height=height)

def main():
    initialize_session_state()
    st.markdown('<h1>Gym Video Recommender 💪</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="subtitle">Find the best fitness videos for your workout</h3>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("## 🧑‍🚀 Fitness Helper")
        query = st.text_input("Ask about workouts:", placeholder="e.g., Muscle gain", value=st.session_state.get('last_query', ''))
        if query:
            response = get_chatbot_response(query)
            st.markdown(response)
            st.session_state.last_query = query
            if query.lower() == "muscle gain":
                st.session_state.recommended_exercises = ["Bench Press", "Squats", "Deadlifts", "Pull-Ups"]
            elif query.lower() == "cardio":
                st.session_state.recommended_exercises = ["Running", "Cycling", "Jump Rope", "Burpees"]
            else:
                st.session_state.recommended_exercises = ["General Workout 1", "General Workout 2", "General Workout 3"]
        
        st.markdown("## ✅ Daily Exercise Plan")
        st.markdown("Mark exercises completed:")
        exercises = {ex: st.checkbox(f"{ex} (15 min)") for ex in st.session_state.recommended_exercises}
        if st.button("Log Exercise", type="secondary"):
            log_exercise(exercises)
            st.success("Exercise logged!")
            today = datetime.date.today()
            logged = [ex for ex, min in st.session_state.exercise_log.get(today, {}).items() if min > 0]
            if logged:
                st.markdown("**Today’s Log**: " + ", ".join(logged))
            else:
                st.markdown("**Today’s Log**: None")
        
        progress_df = get_progress_data()
        if not progress_df.empty:
            st.markdown("### Weekly Progress")
            st.write("Total exercise minutes per day this week.")
            chart = {
                "type": "bar",
                "data": {
                    "labels": progress_df["Date"].tolist(),
                    "datasets": [{
                        "label": "Workout Time",
                        "data": progress_df["Minutes"].tolist(),
                        "backgroundColor": "#28a745",
                        "borderColor": "#218838",
                        "borderWidth": 1
                    }]
                },
                "options": {
                    "scales": {
                        "y": {"beginAtZero": True, "title": {"display": True, "text": "Minutes"}},
                        "x": {"title": {"display": True, "text": "Date"}}
                    },
                    "plugins": {
                        "legend": {"display": True, "position": "top"},
                        "title": {"display": True, "text": "Weekly Workout Progress"}
                    }
                }
            }
            render_chart(chart, "weekly_progress")
        
        dist_df = get_exercise_distribution()
        if not dist_df.empty:
            st.markdown("### Exercise Mix")
            st.write("How often each exercise was completed.")
            pie_chart = {
                "type": "pie",
                "data": {
                    "labels": dist_df["Exercise"].tolist(),
                    "datasets": [{
                        "data": dist_df["Days Completed"].tolist(),
                        "backgroundColor": ["#28a745", "#ff6f00", "#1a3c87", "#d81b60"],
                        "borderColor": "#fff",
                        "borderWidth": 1
                    }]
                },
                "options": {
                    "plugins": {
                        "legend": {"position": "right"},
                        "title": {"display": True, "text": "Exercise Breakdown"}
                    }
                }
            }
            render_chart(pie_chart, "exercise_dist")
        
        weekly_total, remaining, daily_needed = predict_progress()
        st.markdown("### Progress Stats")
        st.markdown(f"- Weekly: {weekly_total} min (Goal: 150)")
        st.markdown(f"- Left: {remaining} min")
        st.markdown(f"- Daily: ~{daily_needed:.1f} min")
        consistency = len([d for d, ex in st.session_state.exercise_log.items() if sum(ex.values()) > 0]) / 7 * 100
        st.markdown(f"- Consistency: {consistency:.1f}%")
    st.markdown("**🔍 Find Workouts**")
    suggestions = get_suggestions()
    keyword = st.selectbox("Keyword:", options=[""] + suggestions, format_func=lambda x: "Select..." if x == "" else x)
    with st.expander("Filters"):
        duration = st.selectbox("Duration", options=["Any"] + list(DURATION_RANGES.keys()))
        workout_type = st.selectbox("Type", options=["Any"] + WORKOUT_TYPES)
        difficulty = st.selectbox("Difficulty", options=["Any"] + DIFFICULTY_LEVELS)
    if st.button("Get Recommendations", type="primary"):
        if keyword:
            search_query = f"gym {keyword}"
            recommendations = get_youtube_recommendations(search_query)
            recommendations = apply_recommendation_filters(recommendations, duration, workout_type, difficulty, {})
            if recommendations:
                export_data = []
                for i, rec in enumerate(recommendations, 1):
                    export_data.append({
                        "Title": rec.title,
                        "Video ID": rec.video_id,
                        "Summary": rec.summary,
                        "Tags": ", ".join([f"{tag.label} ({tag.confidence})" for tag in rec.tags])
                    })
                    st.write(f"### {i}. {rec.title}")
                    st.video(f"https://youtu.be/{rec.video_id}")
                    st.markdown(f"**Summary**: {rec.summary}")
                    st.markdown(f"**Tags**: {', '.join([f'{tag.label} ({tag.confidence})' for tag in rec.tags])}")
                    st.markdown(f"[▶️ YouTube](https://youtu.be/{rec.video_id})")
                    st.divider()
                csv_file = save_to_csv(export_data)
                st.download_button("Download CSV", csv_file, "recommendations.csv", "text/csv")
            else:
                st.error("No videos found.")
        else:
            st.warning("Enter a keyword.")

if __name__ == "__main__":
    main()