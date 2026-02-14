import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import json
import re

# Configuration
load_dotenv(override=True)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
model_id = "llama-3.3-70b-versatile"

st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🤖", layout="centered")

# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

if "step" not in st.session_state:
    st.session_state.step = "greeting"

if "candidate" not in st.session_state:
    st.session_state.candidate = {
        "name": None,
        "email": None,
        "phone": None,
        "experience": None,
        "role": None,
        "location": None,
        "tech_stack": []
    }

if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_q_idx" not in st.session_state:
    st.session_state.current_q_idx = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

if "scores" not in st.session_state:
    st.session_state.scores = []

if "sentiment" not in st.session_state:
    st.session_state.sentiment = "Neutral"

if "language" not in st.session_state:
    st.session_state.language = "English"

# Helper Functions
def analyze_sentiment_and_language(text):
    prompt = f"""
    Analyze the following text from a job candidate.
    Text: "{text}"
    
    1. Identify Sentiment: Positive, Neutral, Concerned, or Confident.
    2. Detect Language: Name of the language.
    
    Return JSON with keys: "sentiment", "language".
    """
    try:
        res = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        data = json.loads(res.choices[0].message.content)
        return data.get("sentiment", "Neutral"), data.get("language", "English")
    except:
        return "Neutral", "English"

def translate_text(text, target_lang):
    if target_lang == "English":
        return text
    
    prompt = f"Translate the following recruitment assistant text to {target_lang}. Keep it professional and friendly. Return ONLY the translated text.\nText: {text}"
    try:
        res = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return res.choices[0].message.content.strip()
    except:
        return text

def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

def check_exit(text):
    exit_keywords = ["exit", "quit", "stop", "bye", "terminate", "goodbye"]
    text_lower = text.lower()
    # Use regex to find whole words only to avoid accidental triggers like "exited"
    for keyword in exit_keywords:
        if re.search(rf"\b{keyword}\b", text_lower):
            return True
    if "end conversation" in text_lower:
        return True
    return False

def get_bot_response(prompt_text):
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt_text}],
            model=model_id,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"I'm sorry, I'm having trouble connecting to my brain. Error: {str(e)}"

# Main Flow Logic
st.markdown("<h1 class='main-title'> TalentScout Hiring Assistant</h1>", unsafe_allow_html=True)

# Sidebar - Settings & Profile
with st.sidebar:
    st.markdown("### 🌐 Settings")
    langs = ["English", "Spanish", "French", "German", "Hindi", "Chinese", "Japanese"]
    # Sync selector with detected language
    try:
        default_lang_idx = langs.index(st.session_state.language)
    except:
        default_lang_idx = 0
        
    selected_lang = st.selectbox("Preferred Language", options=langs, index=default_lang_idx)
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.rerun()

    st.markdown("---")
    st.markdown("### 📑 Candidate Profile")
    with st.container():
        st.markdown(f"""
        <div class="sidebar-card">
            <b>Name:</b> {st.session_state.candidate['name'] or '---'}<br>
            <b>Experience:</b> {st.session_state.candidate['experience'] or '---'} yrs<br>
            <b>Role:</b> {st.session_state.candidate['role'] or '---'}<br>
            <b>Tech Stack:</b> {', '.join(st.session_state.candidate['tech_stack']) or '---'}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Advanced Stats
    st.markdown("### 🧠 AI Insights")
    st.markdown(f"""
    <div class="sidebar-card">
        <b>Detected Mood:</b> {st.session_state.sentiment}<br>
        <b>Primary Language:</b> {st.session_state.language}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Progress Tracker
    steps = ["greeting", "get_email", "get_phone", "get_experience", "get_role", "get_location", "get_tech_stack", "interview", "report"]
    try:
        current_step_idx = steps.index(st.session_state.step)
        progress = (current_step_idx + 1) / len(steps)
        st.write(f"**Interview Progress: {int(progress*100)}%**")
        st.progress(progress)
    except:
        st.progress(1.0)

    st.markdown("---")
    if st.button("Reset Conversation", use_container_width=True):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

# Display Chat Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Greeting
if st.session_state.step == "greeting" and not st.session_state.messages:
    welcome_text_en = """
    Hello! 👋 I'm your **TalentScout Hiring Assistant**. 
    
    My purpose is to help our recruiting team get to know you better by:
    1. Gathering your professional background and tech stack.
    2. Conducting a short, tailored technical screening based on your expertise.
    3. Providing a summary of our conversation to our human recruiters.
    
    *Note: You can type **'exit'** or **'quit'** at any time to end this conversation.*
    
    To get started, could you please tell me your **full name**?
    """
    welcome_text = translate_text(welcome_text_en, st.session_state.language)
    add_message("assistant", welcome_text)
    st.rerun()

# Chat Input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Analyze Sentiment and Language
    st.session_state.sentiment, st.session_state.language = analyze_sentiment_and_language(user_input)

    # Handle Global Exit Keywords
    if check_exit(user_input):
        add_message("user", user_input)
        add_message("assistant", "I understand you'd like to end the conversation. Thank you for your time today! Your session has been closed. Have a great day! 👋")
        st.session_state.step = "completed"
        st.rerun()

    if st.session_state.step == "completed":
        st.warning("The conversation has ended. Please refresh the page to start over.")
        st.stop()

    # Process Input based on current step
    add_message("user", user_input)

    if st.session_state.step == "greeting":
        st.session_state.candidate["name"] = user_input
        msg = translate_text(f"Nice to meet you, {user_input}! What is your **email address**?", st.session_state.language)
        add_message("assistant", msg)
        st.session_state.step = "get_email"
        
    elif st.session_state.step == "get_email":
        st.session_state.candidate["email"] = user_input
        msg = translate_text("Got it. And what is your **phone number**?", st.session_state.language)
        add_message("assistant", msg)
        st.session_state.step = "get_phone"

    elif st.session_state.step == "get_phone":
        st.session_state.candidate["phone"] = user_input
        msg = translate_text("Great. How many **years of experience** do you have in the tech industry?", st.session_state.language)
        add_message("assistant", msg)
        st.session_state.step = "get_experience"

    elif st.session_state.step == "get_experience":
        try:
            exp = int(''.join(filter(str.isdigit, user_input)))
            st.session_state.candidate["experience"] = exp
            msg = translate_text("What **position** are you applying for?", st.session_state.language)
            add_message("assistant", msg)
            st.session_state.step = "get_role"
        except:
            msg = translate_text("I didn't quite catch that. Please provide the number of years as a digit.", st.session_state.language)
            add_message("assistant", msg)

    elif st.session_state.step == "get_role":
        st.session_state.candidate["role"] = user_input
        msg = translate_text("Where are you **currently located**?", st.session_state.language)
        add_message("assistant", msg)
        st.session_state.step = "get_location"

    elif st.session_state.step == "get_location":
        st.session_state.candidate["location"] = user_input
        msg = translate_text("Excellent. Finally, please list your **tech stack** (languages, frameworks, tools) separated by commas.", st.session_state.language)
        add_message("assistant", msg)
        st.session_state.step = "get_tech_stack"

    elif st.session_state.step == "get_tech_stack":
        tech_list = [t.strip() for t in user_input.split(",")]
        st.session_state.candidate["tech_stack"] = tech_list
        
        msg = translate_text("Thank you for sharing your background! I'm now generating some tailored technical questions for you. Please wait a moment...", st.session_state.language)
        add_message("assistant", msg)
        st.session_state.step = "generate_questions"
        st.rerun()

    elif st.session_state.step == "interview":
        # Handle the answer to the current question
        current_idx = st.session_state.current_q_idx
        question = st.session_state.questions[current_idx]
        
        # Fallback check for "I don't know" type answers
        if len(user_input.split()) < 2:
             # Very short answer might need a nudge
             pass

        # Evaluate using LLM
        eval_prompt = f"""
        Evaluate the following answer on scale 1-5 for clarity, technical accuracy, and depth.
        Candidate: {st.session_state.candidate['name']}
        Question: {question}
        Answer: {user_input}
        
        IMPORTANT: The feedback/scoring logic must remain internal, but respond to the JSON request.
        Return JSON with keys: 'clarity', 'technical_accuracy', 'depth'.
        """
        try:
            with st.status("📝 Evaluating your response...", expanded=False):
                eval_res = client.chat.completions.create(
                    messages=[{"role": "user", "content": eval_prompt}],
                    model=model_id,
                    response_format={"type": "json_object"}
                )
            score = json.loads(eval_res.choices[0].message.content)
            st.session_state.scores.append(score)
            st.session_state.answers.append(user_input)
            
            # Personalize the transition
            encouragement_prompt = f"The candidate {st.session_state.candidate['name']} just answered a question. Briefly say 'Got it' or 'Thanks' in {st.session_state.language} to keep it natural."
            encouragement = get_bot_response(encouragement_prompt)
            add_message("assistant", encouragement)
            
            st.session_state.current_q_idx += 1
            st.rerun()
        except Exception as e:
            msg = translate_text("I'm having a technical glitch evaluating that answer. Moving to the next question for now.", st.session_state.language)
            add_message("assistant", msg)
            st.session_state.scores.append({"clarity": 1, "technical_accuracy": 1, "depth": 1})
            st.session_state.answers.append(user_input)
            st.session_state.current_q_idx += 1
            st.rerun()

    st.rerun()

# Separate logic for automated transitions (no user input needed)
if st.session_state.step == "generate_questions":
    candidate = st.session_state.candidate
    difficulty = "advanced" if candidate["experience"] >= 5 else "intermediate" if candidate["experience"] >= 2 else "basic"
    
    ctx = f"Candidate: {st.session_state.candidate['name']}, Role: {st.session_state.candidate['role']}, Lang: {st.session_state.language}"
    prompt = f"""
    You are a technical interviewer named TalentScout. 
    Context: {ctx}
    Based on this stack: {candidate['tech_stack']}, generate exactly 4-5 interview questions.
    Difficulty: {difficulty}.
    IMPORTANT: Respond in {st.session_state.language}.
    Return JSON: {{"questions": ["..."]}}
    """
    
    try:
        with st.status("🧠 Analyzing your profile and generating technical questions...", expanded=True) as status:
            st.write("Reviewing tech stack...")
            tech_stack_str = ", ".join(candidate['tech_stack'])
            st.write(f"Formulating {difficulty} level questions for {tech_stack_str}...")
            
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model_id,
                response_format={"type": "json_object"}
            )
            st.session_state.questions = json.loads(response.choices[0].message.content)["questions"]
            status.update(label=translate_text("✅ Questions Ready!", st.session_state.language), state="complete", expanded=False)
            
        st.session_state.step = "interview"
        msg = translate_text(f"I've prepared {len(st.session_state.questions)} questions for you. Let's start!", st.session_state.language)
        add_message("assistant", msg)
        st.rerun()
    except Exception as e:
        msg = translate_text(f"I encountered an error generating questions: {str(e)}. Please type 'restart' to try again.", st.session_state.language)
        add_message("assistant", msg)
        st.session_state.step = "error"

if st.session_state.step == "interview":
    idx = st.session_state.current_q_idx
    if idx < len(st.session_state.questions):
        # We need to check if we just transitioned to this index
        if len(st.session_state.messages) == 0 or st.session_state.messages[-1]["content"] != st.session_state.questions[idx]:
             add_message("assistant", st.session_state.questions[idx])
             st.rerun()
    else:
        st.session_state.step = "report"
        st.rerun()

if st.session_state.step == "report":
    scores = st.session_state.scores
    avg_score = sum((s["clarity"] + s["technical_accuracy"] + s["depth"]) / 3 for s in scores) / len(scores)
    
    report_prompt = f"""
    Generate a polite closing summary for {st.session_state.candidate['name']} in {st.session_state.language}.
    Mention they scored {round(avg_score, 2)}/5 on average.
    Thank them and mention human recruiters will be in touch.
    """
    closing_msg = get_bot_response(report_prompt)
    
    add_message("assistant", closing_msg)
    st.session_state.step = "completed"
    st.rerun()


