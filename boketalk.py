import streamlit as st
import openai
from langdetect import detect

# API key is obtained from the Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def detect_language(text):
    return detect(text)

def translate(text, target_language): 
    prompt =f"Translate the following {'English' if target_language == 'ja' else 'Japanese'} text to {'Japanese／日本語でお願いします。' if target_language == 'ja' else 'English'}:\n{text}"
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def generate_joke(text): 
    prompt =f"Create a puzzle-like joke based on this text:\n{text}"
    messages = [{"role": "user", "content": prompt}]
#    

#    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


st.title("TOKYO Boke Talk／東京ボケトーク")

st.markdown(
"""
-- ver.0.291 -- 2023/08/15 [@hortense667](https://twitter.com/hortense667)　 
"""
)

#---------------------------------------------------------------------
#def init_messages():
#    clear_button = st.sidebar.button("Clear Conversation", key="clear")
#    if clear_button or "messages" not in st.session_state:
#        st.session_state.messages = [
#            SystemMessage(content="You are a helpful assistant.")
#        ]
#        st.session_state.costs = []

def select_model():
    model = st.sidebar.radio("Language model:", ("GPT-3.5-turbo", "GPT-4"))
    if model == "GPT-3.5-turbo":
        model_name = "gpt-3.5-turbo"
    else:
        model_name = "gpt-4"

    # サイドバーにスライダーを追加し、temperatureを0から2までの範囲で選択可能にする
    # 初期値は0.0、刻み幅は0.1とする
    temperature = st.sidebar.slider("Temperature:", min_value=0.0, max_value=2.0, value=0.0, step=0.01)

    return ChatOpenAI(temperature=temperature, model_name=model_name)

# サイドバーのタイトルを表示
st.sidebar.title("Options")

# Streamlitはmarkdownを書けばいい感じにHTMLで表示してくれます
# (もちろんメイン画面でも使えます)
#st.sidebar.markdown("## Costs")
#st.sidebar.markdown("**Total cost**")
#for i in range(3):
#    st.sidebar.markdown(f"- ${i+0.01}")  # 説明のためのダミー

#サイドバーからモデルを選ぶ
llm = select_model()
#コストはいま使わないので不要
#init_messages()

#---------------------------------------------------------------------

text = st.text_input("Enter some text")
if st.button("Translate and Generate Joke"):
    if text:
        target_language = 'ja' if detect_language(text) == 'en' else 'en'
        translation = translate(text, target_language)
        joke = generate_joke(text)
        st.write("Translation:", translation)
        st.write("Joke:", joke)
    else:
        st.write("Please enter some text.")
if st.button("Clear"):
    text = ""
    st.empty()
