import streamlit as st
import asyncio
from client import MCPClient

# Configuration de la page
st.set_page_config(
    page_title="Spotify MCP Chat",
    page_icon="🎵",
    layout="centered"
)

# Titre
st.title("🎵 Spotify MCP Assistant")
st.caption("Powered by Google Gemini & Model Context Protocol")

# Initialiser l'historique de chat dans la session
if "messages" not in st.session_state:
    st.session_state.messages = []

if "client" not in st.session_state:
    st.session_state.client = MCPClient()

# Afficher l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utilisateur
if prompt := st.chat_input("Ask me about Spotify artists..."):
    # Ajouter le message utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Afficher le message utilisateur
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Simuler une réponse (à remplacer par votre logique MCP)
    with st.chat_message("assistant"):
        response = asyncio.run(st.session_state.client.run(prompt))
        st.markdown(response)
    
    # Ajouter la réponse à l'historique
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar avec infos
with st.sidebar:
    st.header("About")
    st.info("""
    This chatbot connects to a Spotify MCP server to help you:
    - 🎤 Find top tracks by artist
    - 📊 Get artist information
    - 🎵 Discover music
    """)
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
