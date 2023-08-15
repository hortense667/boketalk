import streamlit as st
import openai
from langdetect import detect

# API key is obtained from the Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def detect_language(text):
    return detect(text)

def translate(text, target_language, model_name, temperature, region): 
    region_prefix_map = {
        "Standard": "",
        "Osaka": "大阪弁で",
        "Kyoto": "京都弁で",
        "Nagoya": "名古屋弁で",
        "Kagoshima": "鹿児島弁で",
        "Tsugaru": "津軽弁で",
        "Okinawa": "沖縄弁で"
    }
    prefix = region_prefix_map[region]
    prompt = f"Translate the following {'English' if target_language == 'ja' else 'Japanese'} text to {prefix} {'Japanese／日本語でお願いします。' if target_language == 'ja' else 'English'}:\n{text}"
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]

def generate_joke(text, model_name, temperature, joke_type, region): 
    region_prefix_map = {
        "Standard": "",
        "Osaka": "大阪弁で",
        "Kyoto": "京都弁で",
        "Nagoya": "名古屋弁で",
        "Kagoshima": "鹿児島弁で",
        "Tsugaru": "津軽弁で",
        "Okinawa": "沖縄弁で"
    }
    prefix = region_prefix_map[region]
    prompt = f"Create a {prefix} {joke_type} joke based on this text:\n{text}" if joke_type not in ['なにも指定しない', '自分で指定する'] else f"Create a {prefix} joke based on this text:\n{text}"
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
model_name = st.sidebar.radio('Choose a language model', ['gpt-4', 'gpt-3.5-turbo'])
temperature = st.sidebar.slider('Temperature', 0.0, 1.0, 0.7)
joke_type_options = ['なにも指定しない', '自分で指定する', 'funny', 'heartworming', 'clean', 'childish', 'witty', 'highbrow', 'droll', 'parody', 'surreal or absurd', 'dad', 'dirty', 'self-deprecating', 'Potty']
joke_type = st.sidebar.selectbox('ジョークの種類', joke_type_options)
regions = ["Standard", "Osaka", "Kyoto", "Nagoya", "Kagoshima", "Tsugaru", "Okinawa"]
region = st.sidebar.selectbox("Region for output dialect", regions)

custom_joke_type = ""
if joke_type == '自分で指定する':
    custom_joke_type = st.sidebar.text_input("ジョークの種類を指定してください")

text = st.text_input("Enter some text")
if st.button("Translate and Generate Joke"):
    if text:
        target_language = 'ja' if detect_language(text) == 'en' else 'en'
        translation = translate(text, target_language, model_name, temperature)
        
        joke_type_to_use = custom_joke_type if joke_type == '自分で指定する' else joke_type
        joke = generate_joke(text, model_name, temperature, joke_type_to_use, region)
        
        st.write("Translation:", translation)
        st.write("Joke:", joke)
    else:
        st.write("Please enter some text.")
