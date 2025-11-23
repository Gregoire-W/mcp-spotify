import streamlit as st
import time
from client import MCPClient
import asyncio
import secrets
import os

# Configuration de la page
st.set_page_config(
    page_title="Spotify Chatbot",
    page_icon="🎵",
    layout="wide"
)

# Init MCP Client
if "client" not in st.session_state:
    st.session_state.client = MCPClient()

# Initialisation du session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Vérifier si Spotify est connecté en fonction du paramètre "code" dans l'URL
if "code" in st.query_params:
    st.session_state.spotify_connected = True
else:
    if "spotify_connected" not in st.session_state:
        st.session_state.spotify_connected = False

# Sidebar
with st.sidebar:
    github_logo = '<svg xmlns="http://www.w3.org/2000/svg" height="20" viewBox="0 0 16 16" fill="currentColor" style="vertical-align: middle; margin-right: 5px;"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>'
    st.markdown(f"<p style='font-size: 1.2em; margin-bottom: 0;'>{github_logo} Built by <a href='https://github.com/Gregoire-W' target='_blank' style='text-decoration: none; color: inherit;'>Gregoire-W</a></p>", unsafe_allow_html=True)
    st.divider()
    
    # Section Tools
    st.subheader("🛠️ Tools")
    
    # Bouton de connexion Spotify
    if not st.session_state.spotify_connected:
        # Générer l'état et le stocker dans la session
        if "spotify_state" not in st.session_state:
            st.session_state.spotify_state = secrets.token_urlsafe(16)
        
        state = st.session_state.spotify_state
        scope = "user-read-private user-read-email playlist-modify-public playlist-modify-private"
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        redirect_uri = "http://127.0.0.1:8080/"
        
        # Construire l'URL d'autorisation
        auth_url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}&state={state}"
        
        # Utiliser un lien qui redirige le navigateur
        st.link_button("🎵 Connect to Spotify", auth_url, use_container_width=True, type="primary")
    else:
        st.success("✅ Connected to Spotify")
        if st.button("🔌 Disconnect", use_container_width=True):
            st.session_state.spotify_connected = False
            # Supprimer le paramètre "code" de l'URL si présent
            if "code" in st.query_params:
                del st.query_params["code"]
            st.rerun()
    
    st.divider()
    
    # Bouton pour clear le chat
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.client.reset_messages()
        st.rerun()
    
    st.divider()
    
    # Exemples de ce que l'assistant peut faire
    st.subheader("💡 Examples")
    with st.container():
        st.markdown("""
        <div style='background-color: rgba(255, 255, 255, 0.05); border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.1);'>
            <p style='margin: 0; padding: 5px 0;'>✨ Create custom playlists</p>
            <p style='margin: 0; padding: 5px 0;'>🎵 Fill playlists with songs</p>
            <p style='margin: 0; padding: 5px 0;'>🎼 Split large playlists by genre</p>
            <p style='margin: 0; padding: 5px 0;'>🔍 Search and discover music</p>
        </div>
        """, unsafe_allow_html=True)

# Zone principale de chat
spotify_logo = '<svg xmlns="http://www.w3.org/2000/svg" height="40" viewBox="0 0 496 512" style="vertical-align: middle; margin-right: 5px;"><path fill="#1DB954" d="M248 8C111.1 8 0 119.1 0 256s111.1 248 248 248 248-111.1 248-248S384.9 8 248 8zm100.7 364.9c-4.2 0-6.8-1.3-10.7-3.6-62.4-37.6-135-39.2-206.7-24.5-3.9 1-9 2.6-11.9 2.6-9.7 0-15.8-7.7-15.8-15.8 0-10.3 6.1-15.2 13.6-16.8 81.9-18.1 165.6-16.5 237 26.2 6.1 3.9 9.7 7.4 9.7 16.5s-7.1 15.4-15.2 15.4zm26.9-65.6c-5.2 0-8.7-2.3-12.3-4.2-62.5-37-155.7-51.9-238.6-29.4-4.8 1.3-7.4 2.6-11.9 2.6-10.7 0-19.4-8.7-19.4-19.4s5.2-17.8 15.5-20.7c27.8-7.8 56.2-13.6 97.8-13.6 64.9 0 127.6 16.1 177 45.5 8.1 4.8 11.3 11 11.3 19.7-.1 10.8-8.5 19.5-19.4 19.5zm31-76.2c-5.2 0-8.4-1.3-12.9-3.9-71.2-42.5-198.5-52.7-280.9-29.7-3.6 1-8.1 2.6-12.9 2.6-13.2 0-23.3-10.3-23.3-23.6 0-13.6 8.4-21.3 17.4-23.9 35.2-10.3 74.6-15.2 117.5-15.2 73 0 149.5 15.2 205.4 47.8 7.8 4.5 12.9 10.7 12.9 22.6 0 13.6-11 23.3-23.2 23.3z"/></svg>'
st.markdown(f"<h1 style='margin-bottom: 0;'>{spotify_logo} Your Intelligent Spotify Assistant</h1>", unsafe_allow_html=True)
st.caption("Powered by Google Gemini & MCP")

# Afficher l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie du message
if prompt := st.chat_input("Ask your question..."):
    # Ajouter le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Générer la réponse de l'assistant
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Afficher les points de suspension pendant la "réflexion"
        with st.spinner(""):
            if st.session_state.spotify_connected:
                full_response = asyncio.run(st.session_state.client.run(prompt, st.query_params["code"]))
            else:
                full_response = asyncio.run(st.session_state.client.run(prompt, ""))
        
        # Afficher la réponse progressivement
        displayed_response = ""
        for char in full_response:
            displayed_response += char
            message_placeholder.markdown(displayed_response + "▌")
            time.sleep(0.01)  # Vitesse d'affichage
        
        # Afficher la réponse finale sans le curseur
        message_placeholder.markdown(full_response)
    
    # Ajouter la réponse à l'historique
    st.session_state.messages.append({"role": "assistant", "content": full_response})
