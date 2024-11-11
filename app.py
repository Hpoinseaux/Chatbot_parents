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
    
    
    # Vérification de la réponse
    if response.status_code == 200:
        return response.json()  # Retourne la réponse JSON si elle est correcte
    else:
        st.error(f"Erreur avec l'API: {response.status_code}")
        return None


st.markdown("<h3 style='text-align: right; font-size: 14px;'>Hadrien Poinseaux</h3>", unsafe_allow_html=True)

# Couleur de fond en utilisant st.markdown pour une section
page_bg_img = '''
<style>
[data-testid="stMain"] {
background-color: #9dcfb6; /* Couleur de fond */
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)




# Ajouter une image au-dessus du titre (liée à l'éducation)
st.image("https://images.unsplash.com/photo-1503676260728-1c00da094a0b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDEwfGVkdWNhdGlvbnxlbnwwfHx8fDE2NDk1Nzc3NjI&ixlib=rb-1.2.1&q=80&w=1080", use_column_width=True)

# Interface Streamlit
st.title("Assistant ASH pour les parents")

st.markdown("""
Je suis votre assistant , conçu pour vous aider à naviguer à travers les questions et les préoccupations concernant les situations des élèves à besoins particuliers. Mon objectif est de vous fournir des informations claires et rassurantes. 
N'hésitez pas à poser vos questions : je suis là pour vous écouter et vous soutenir à chaque étape de votre parcours. Que ce soit pour des conseils, des informations sur les procédures ou des ressources, je suis ici pour vous aider !
""")


# Initialiser l'état de session pour l'historique de la conversation
if 'historique' not in st.session_state:
    st.session_state['historique'] = []
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = "user123"  # Peut être un identifiant unique pour chaque utilisateur

# Afficher l'historique de la conversation
for message in st.session_state['historique']:
    if message['role'] == 'user':
        st.write(f"**Moi:** {message['message']}")
    else:
        st.write(f"**assistant ASH:** {message['message']}")

# Afficher la barre de texte et le bouton d'envoi en bas de la page
placeholder = st.empty()  # Crée un espace réservé en bas de la page

with placeholder.container():
    # Saisie de texte et bouton Envoyer
    message = st.text_input("Poser vos questions:")
    if st.button("Envoyer"):
        if message:
             # Ajouter le message de l'utilisateur à l'historique avant de faire l'appel
            st.session_state['historique'].append({"role": "user", "message": message})
            # Envoyer la requête au chatbot Voiceflow
            reponse = envoyer_message(st.session_state['user_id'], message)
            
            if reponse:
                # Ajouter le message de l'utilisateur à l'historique
                st.session_state['historique'].append({"role": "user", "message": message})
        
                # Parcourir chaque événement dans la réponse
                for event in reponse:
                    # Vérifier que c'est bien un type "text" et que "payload" contient "message"
                    if event.get("type") == "text" and "payload" in event:
                        st.session_state['historique'].append({"role": "bot", "message": event["payload"]["message"]})

            # Rechargement pour garder le champ de texte et le bouton en bas
            st.experimental_set_query_params(keep=True)