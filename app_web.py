import streamlit as st
import requests
from groq import Groq  

# --- CORE LOGIC (Kept identical to your CLI app) ---

def get_news(topic, news_api_key):
    url = f'https://newsapi.org/v2/everything?q={topic}&apiKey={news_api_key}&pageSize=5'
    response = requests.get(url)
    data = response.json()
    return data  

def extract_headlines(news):
    # Quick guard rail in case NewsAPI returns an error message instead of articles
    if 'articles' not in news:
        return []
    articles = news['articles']
    headlines = []
    for article in articles:
        headlines.append(article['title'])
    return headlines

def generate_briefing(headlines, groq_api_key):
    client = Groq(api_key=groq_api_key)
    prompt = f'Based on this headlines list: {headlines} generate a clean, executive 3 point briefing'
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response.choices[0].message.content

# --- STREAMLIT WEB INTERFACE ---

st.set_page_config(page_title="AI Briefing Agent", page_icon="📰", layout="centered")

st.title("📰 Autonomous AI News Briefing Agent")
st.caption("Powered by Groq Llama-3.3 & NewsAPI")
st.write("---")

# Sidebar for secure API Key input instead of hardcoding them
st.sidebar.header("🔑 API Authentication")
news_key = st.sidebar.text_input("Enter NewsAPI Key:", type="password")
groq_key = st.sidebar.text_input("Enter Groq API Key:", type="password")

# Web input form replacing 'topic = input()'
topic = st.text_input("🎯 Enter a topic you want an intelligence briefing on:", placeholder="e.g., Blockchain, AI Startups, Bengaluru Tech")

# Action Button
if st.button("Generate Web Briefing", type="primary"):
    # Guard clause to ensure keys and topic exist
    if not news_key or not groq_key:
        st.error("Please add both your NewsAPI and Groq API keys in the sidebar to run the agent.")
    elif not topic.strip():
        st.warning("Please enter a valid topic.")
    else:
        # Visual loading spinner inside Chrome
        with st.spinner(f"Agent actively fetching and analyzing news on '{topic}'..."):
            try:
                # Step 1 & 2: Fetch and Extract
                raw_news = get_news(topic, news_key)
                headlines = extract_headlines(raw_news)
                
                if not headlines:
                    st.error("No articles found for this topic. Check your NewsAPI key or topic query.")
                else:
                    # Step 3: Run AI inference
                    briefing = generate_briefing(headlines, groq_key)
                    
                    # Step 4: Output cleanly to Chrome web UI
                    st.success("Briefing Generated successfully!")
                    st.markdown("### 🤖 Executive AI Briefing")
                    st.info(briefing)
                    
                    # Optional: Allow user to download the file directly from Chrome
                    st.download_button(
                        label="📥 Download Briefing as Text File",
                        data=f"Topic: {topic}\n==================================================\n{briefing}",
                        file_name=f"{topic.replace(' ', '_')}_briefing.txt",
                        mime="text/plain"
                    )
            except Exception as e:
                st.error(f"Execution Error: {e}")