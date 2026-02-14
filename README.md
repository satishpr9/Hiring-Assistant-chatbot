# TalentScout Hiring Assistant 🤖

## Project Overview
**TalentScout Hiring Assistant** is an advanced AI-powered recruitment tool designed to automate and enhance the initial stages of the hiring process. Built using **Streamlit** and powered by **Groq's Llama-3.3-70b** model, this chatbot acts as a first-line interviewer that:
- Seamlessly gathers candidate personal and professional information.
- Conducts a tailored technical screening based on the candidate's specific tech stack and experience level.
- Analyzes candidate sentiment and supports multiple languages.
- Generates a comprehensive evaluation for human recruiters.

## Installation Instructions

### Prerequisites
- Python 3.8 or higher.
- A Groq API Key (get it from [Groq Console](https://console.groq.com/)).

### Steps
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd talentscout_app
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**:
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_actual_api_key_here
   ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Usage Guide
1. **Introduction**: Start by providing your name when prompted by the assistant.
2. **Information Gathering**: The bot will ask for your email, phone, years of experience, desired role, and location.
3. **Tech Stack**: List your technical skills (e.g., Python, React, AWS) separated by commas.
4. **Technical Interview**: The bot will generate 4-5 specialized questions based on your profile. Answer them as clearly as possible.
5. **Real-time Feedback**: The sidebar will display your detected mood and language.
6. **Completion**: Once finished, the bot will provide a summary and close the session.

## Technical Details
- **Frontend**: [Streamlit](https://streamlit.io/) for a fast, interactive web interface.
- **LLM Engine**: [Groq](https://groq.com/) using the `llama-3.3-70b-versatile` model for lightning-fast inference.
- **Styling**: Custom CSS (`style.css`) for a modern, professional chat experience.
- **Architecture**:
  - **Session State Management**: Tracks interview steps, candidate data, and chat history.
  - **Sentiment Analysis**: Real-time analysis of candidate responses to gauge confidence and engagement.
  - **Multi-lingual Support**: Automatic language detection and translation for global accessibility.

## Prompt Design
The core intelligence of TalentScout lies in its carefully crafted prompts:
- **Information Gathering**: Prompts are designed to be friendly yet professional, ensuring high conversion rates during the data collection phase.
- **Dynamic Question Generation**:
  ```text
  Context: Candidate Role, Experience, Tech Stack.
  Task: Generate 4-5 technical questions at a [Basic/Intermediate/Advanced] level.
  Constraint: Output strictly in JSON format.
  ```
- **Evaluation**: The bot uses an internal scoring prompt to evaluate clarity, technical accuracy, and depth of answers without exposing the raw scores to the candidate immediately.

## Challenges & Solutions
- **Challenge**: Managing complex conversation state in a stateless web environment.
  - **Solution**: Leveraged Streamlit's `session_state` to create a robust finite state machine for the interview flow.
- **Challenge**: Providing a consistent multi-lingual experience.
  - **Solution**: Integrated a dedicated translation and language detection layer within the LLM calls to ensure the bot responds in the candidate's preferred language.
- **Challenge**: Ensuring question relevance.
  - **Solution**: Implemented a "Difficulty Filter" based on years of experience to tailor the technical rigor appropriately.

---
*Developed for modern recruitment teams to focus more on people and less on screening.*
# Hiring-Assistant-chatbot
