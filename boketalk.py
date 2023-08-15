import streamlit as st
import openai
from langdetect import detect

# API key is obtained from the Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def detect_language(text):
    return detect(text)

def translate(text, target_language, model_name, temperature): 
    prompt = f"Translate the following {'English' if target_language == 'ja' else 'Japanese'} text to {'Japanese／日本語でお願いします。' if target_language == 'ja' else 'English'}:\n{text}"
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]

def generate_joke(text, model_name, temperature, joke_type): 
    prompt = f"Create a {joke_type} joke based on this text:\n{text}" if joke_type != 'なにも指定しない' else f"Create a joke based on this text:\n{text}"
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]

st.title("TOKYO Boke Talk／東京ボケトーク")

st.markdown(
"""
-- ver.0.291 -- 2023/08/15 [@hortense667](https://twitter.com/hortense667)
"""
)

# Sidebar for options
st.sidebar.title("オプション設定")
model_name = st.sidebar.radio('言語モデル', ['gpt-3.5-turbo','gpt-4'])
temperature = st.sidebar.slider('創造性（Temperature）', 0.0, 1.0, 0.7)
joke_type = st.sidebar.selectbox('ジョークの種類', ['なにも指定しない', 'funny', 'heartworming', 'clean', 'childish', 'witty', 'highbrow', 'droll', 'parody', 'surreal or absurd', 'dad', 'dirty', 'self-deprecating', 'Potty'])

text = st.text_input("Enter some text")
if st.button("Translate and Generate Joke"):
    if text:
        target_language = 'ja' if detect_language(text) == 'en' else 'en'
        translation = translate(text, target_language, model_name, temperature)
        joke = generate_joke(text, model_name, temperature, joke_type)
        st.write("Translation:", translation)
        st.write("Joke:", joke)
    else:
        st.write("Please enter some text.")
if st.button("Clear"):
    text = ""
    st.empty()
