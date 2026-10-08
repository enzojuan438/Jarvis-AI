import sys
import subprocess

# Instala automaticamente a biblioteca da OpenAI se não estiver presente no servidor
try:
    from openai import OpenAI
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
    from openai import OpenAI

import streamlit as st

# Configuração da página do Streamlit
st.set_page_config(page_title="J.A.R.V.I.S. AI", page_icon="🤖", layout="centered")

st.title("🤖 J.A.R.V.I.S.")
st.subheader("Just A Rather Very Intelligent System")
st.write("À sua disposição, **Senhor Enzo Aura**. Como posso ajudá-lo hoje?")

# Sua API Key inserida diretamente e de forma fixa no código
API_KEY = "AQ.Ab8RN6LwshWXwhpTSLni4l-KJgZvlwERSJLFAHh-oy_EfnkUtw"

# Inicializa o cliente da OpenAI
client = OpenAI(api_key=API_KEY)

# Define a personalidade do JARVIS direcionada ao Enzo Aura
JARVIS_PROMPT = (
    "Você é o J.A.R.V.I.S., a inteligência artificial avançada criada por Tony Stark. "
    "Seu mestre absoluto e único usuário autorizado chama-se Enzo Aura. "
    "Seu tom deve ser extremamente polido, britânico, prestativo, altamente inteligente e leal. "
    "Sempre trate o usuário como 'Senhor Enzo Aura' ou 'Senhor'. "
    "Use respostas elegantes, eficientes e demonstre capacidades tecnológicas de ponta em sua linguagem."
)

# Inicializa o histórico de mensagens se não existir
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": JARVIS_PROMPT}
    ]

# Exibe as mensagens anteriores do chat (escondendo o prompt do sistema)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Entrada de texto do usuário
if prompt := st.chat_input("O que deseja, Senhor Enzo Aura?"):
    # Exibe a mensagem do usuário
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Adiciona a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Solicita a resposta do modelo
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Faz a chamada para a API usando o modelo gpt-4o-mini
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            stream=True,
        )
        
        # Transmite a resposta em tempo real (Stream)
        for chunk in response:
            if chunk.choices.delta.content:
                full_response += chunk.choices.delta.content
                message_placeholder.markdown(full_response + "▌")
                
        message_placeholder.markdown(full_response)
        
    # Adiciona a resposta do JARVIS ao histórico
    st.session_state.messages.append({"role": "assistant", "content": full_response})
