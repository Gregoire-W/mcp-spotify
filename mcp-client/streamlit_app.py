import streamlit as st
import asyncio
from client import MCPClient
import secrets

# Configuration de la page
st.set_page_config(
    page_title="Spotify MCP Chat",
    page_icon="🎵",
    layout="centered"
)

# Titre
st.title("🎵 Spotify MCP Assistant")
st.caption("Powered by Google Gemini & Model Context Protocol")

if "client" not in st.session_state:
    st.session_state.client = MCPClient()

# Initialiser l'historique de chat dans la session
if "messages" not in st.session_state:
    st.session_state.messages = []

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
        if "code" in st.query_params:
            response = asyncio.run(st.session_state.client.run(prompt, st.query_params["code"]))
        else:
            response = asyncio.run(st.session_state.client.run(prompt, ""))
        st.markdown(response)
    
    # Ajouter la réponse à l'historique
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar avec infos
with st.sidebar:
    st.header("🔧 Tools")
    
    # Spotify logo SVG
    spotify_logo = '<svg xmlns="http://www.w3.org/2000/svg" height="16" viewBox="0 0 496 512" style="vertical-align: middle; margin-right: 5px;"><path fill="#1DB954" d="M248 8C111.1 8 0 119.1 0 256s111.1 248 248 248 248-111.1 248-248S384.9 8 248 8zm100.7 364.9c-4.2 0-6.8-1.3-10.7-3.6-62.4-37.6-135-39.2-206.7-24.5-3.9 1-9 2.6-11.9 2.6-9.7 0-15.8-7.7-15.8-15.8 0-10.3 6.1-15.2 13.6-16.8 81.9-18.1 165.6-16.5 237 26.2 6.1 3.9 9.7 7.4 9.7 16.5s-7.1 15.4-15.2 15.4zm26.9-65.6c-5.2 0-8.7-2.3-12.3-4.2-62.5-37-155.7-51.9-238.6-29.4-4.8 1.3-7.4 2.6-11.9 2.6-10.7 0-19.4-8.7-19.4-19.4s5.2-17.8 15.5-20.7c27.8-7.8 56.2-13.6 97.8-13.6 64.9 0 127.6 16.1 177 45.5 8.1 4.8 11.3 11 11.3 19.7-.1 10.8-8.5 19.5-19.4 19.5zm31-76.2c-5.2 0-8.4-1.3-12.9-3.9-71.2-42.5-198.5-52.7-280.9-29.7-3.6 1-8.1 2.6-12.9 2.6-13.2 0-23.3-10.3-23.3-23.6 0-13.6 8.4-21.3 17.4-23.9 35.2-10.3 74.6-15.2 117.5-15.2 73 0 149.5 15.2 205.4 47.8 7.8 4.5 12.9 10.7 12.9 22.6 0 13.6-11 23.3-23.2 23.3z"/></svg>'
    
    # Spotify Connection
    if "spotify_connected" not in st.session_state:
        st.session_state.spotify_connected = False
    
    if not st.session_state.spotify_connected:
        # Générer l'état et le stocker dans la session
        if "spotify_state" not in st.session_state:
            st.session_state.spotify_state = secrets.token_urlsafe(16)
        
        state = st.session_state.spotify_state
        scope = "user-read-private user-read-email playlist-modify-public playlist-modify-private"
        client_id = "5f16e4a08bf441158bf995c7a8276bd0"
        redirect_uri = "http://127.0.0.1:8080/"
        
        # Construire l'URL d'autorisation
        auth_url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}&state={state}"
        
        # Utiliser un lien qui redirige le navigateur
        st.link_button("🎵 Connect to Spotify", auth_url, use_container_width=True, type="primary")
    else:
        if st.button("Disconnect from Spotify", key="spotify_disconnect", use_container_width=True):
            st.session_state.spotify_connected = False
            st.rerun()
    
    st.divider()
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.client.reset_messages()
        st.rerun()
