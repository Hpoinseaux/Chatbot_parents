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
    
    # Effectuer la requête
    response = requests.post(url, json=data, headers=headers)
    
    # Afficher le code de statut HTTP pour diagnostiquer les erreurs
    st.write(f"Status Code: {response.status_code}")
    
    # Afficher la réponse brute pour voir la structure complète
    st.write(response.text)
    
    # Vérification de la réponse
    if response.status_code == 200:
        return response.json()  # Retourne la réponse JSON si elle est correcte
    else:
        st.error(f"Erreur avec l'API: {response.status_code}")
        return None

# Interface Streamlit
st.title("Chatbot Voiceflow avec Streamlit")

if 'historique' not in st.session_state:
    st.session_state['historique'] = []
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = "user123"  # Peut être un identifiant unique pour chaque utilisateur

message = st.text_input("Tu peux poser une question:")

if st.button("Envoyer"):
    if message:
        # Envoyer la requête au chatbot Voiceflow
        reponse = envoyer_message(st.session_state['user_id'], message)
        
        if reponse:
            # Ajouter le message de l'utilisateur à l'historique
            st.session_state['historique'].append({"role": "user", "message": message})
            
            # Vérifier que la réponse est une liste et la parcourir
            if isinstance(reponse, list):
                for event in reponse:  # Parcourir directement la liste
                    if isinstance(event, dict) and event.get("type") == "speak":
                        st.session_state['historique'].append({"role": "bot", "message": event["payload"]["message"]})

# Afficher l'historique de la conversation
for message in st.session_state['historique']:
    if message['role'] == 'user':
        st.write(f"**Toi:** {message['message']}")
    else:
        st.write(f"**Bot:** {message['message']}")