import streamlit as st
import requests

# Configuration de l'API Voiceflow
API_KEY = "VF.DM.671a045c21ddde63559a41cf.7jM8hYY9yfeP49f2"  # Remplace par ta clé API Voiceflow
VERSION_ID = "6719ff054691e037ca52e0ec"  # Remplace par l'ID de version de ton projet

BASE_URL = f"https://general-runtime.voiceflow.com/state/{VERSION_ID}/user"

def envoyer_message(user_id, message):
    url = f"{BASE_URL}/{user_id}/interact"
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "request": {
            "type": "text",
            "payload": message
        }
    }
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erreur avec l'API: {response.status_code}")
        return None

# Interface Streamlit
st.title("Chatbot Voiceflow avec Streamlit")

# Initialisation de l'historique
if 'historique' not in st.session_state:
    st.session_state['historique'] = []
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = "user123"  # Un identifiant unique pour chaque utilisateur

# Affichage de l'historique des messages
for message in st.session_state['historique']:
    if message['role'] == 'user':
        st.write(f"**Toi:** {message['message']}")
    else:
        st.write(f"**Bot:** {message['message']}")

# Barre de message en bas de la page
message = st.text_input("Tu peux poser une question:", key="input_message")

if st.button("Envoyer"):
    if message:
        # Envoyer le message à Voiceflow et obtenir la réponse
        reponse = envoyer_message(st.session_state['user_id'], message)
        
        if reponse:
            # Ajouter le message de l'utilisateur à l'historique
            st.session_state['historique'].append({"role": "user", "message": message})
            
            # Ajouter la réponse du bot à l'historique
            for event in reponse:
                if event.get("type") == "text" and "payload" in event:
                    st.session_state['historique'].append({"role": "bot", "message": event["payload"]["message"]})
        
        # Effacer le champ de texte après l'envoi
        st.session_state.input_message = ""
        
        # Redessiner la page pour afficher le nouvel historique
        st.experimental_rerun()