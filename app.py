from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai


genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

model = genai.GenerativeModel('gemini-pro')

chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

st.set_page_config(page_title='QnA ChatBot')
st.header('QnA ChatBot With History Using Gemini Pro LLM Model')

# initiate session state for chat history if it doesn't exits
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
    
input = st.text_input('Ask your question ...', key='input')
submit = st.button('Ask your question')

if submit and input:
    response = get_gemini_response(input)
    # add user query and response to session  chat history
    st.session_state['chat_history'].append(("You",input))
    st.subheader('The response is ...')
    
    for chunk in response:
        st.success(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))
        
st.subheader('The chat history is ....')

for role,text in st.session_state['chat_history']:
    st.success(f"{role}:{text}")