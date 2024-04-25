import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
senha = os.getenv('API_PASSWORD')

# Configuração do modelo da API
genai.configure(api_key=senha)
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Iniciar a conversa
convo = model.start_chat(history=[
    {
        "role": "user",
        "parts": ["Você é um chatbot amigável e que responderá dúvidas sobre câncer. Você estará funcionando em site que vive de doações: \"http://www.juntoscontraocancer.org.br/\". Identifique quando uma pergunta sobre o assunto for feita e responda-a. Caso não haja perguntas, apenas retorne uma recepção amigável e pergunte como poderia ajudar."]
    },
    {
        "role": "model",
        "parts": ["Olá! 👋 Seja bem-vindo ao juntoscontraocancer.org.br! 💖 Aqui você encontra informações e apoio para enfrentar o câncer. Como posso te ajudar hoje? 😊"]
    },
])

# Interface Streamlit
st.title("Chatbot para Apoio sobre Câncer 💖")
user_input = st.text_input("Digite sua pergunta aqui 🤔", "")
if user_input:
    convo.send_message(user_input)
    response = convo.last.text
    st.write("Resposta:", response)
