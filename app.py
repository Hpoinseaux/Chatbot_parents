import streamlit as st
import cohere

# Initialisation du client Cohere avec la clé API
cohere_api_key = st.secrets["COHERE_API_KEY"]
if not cohere_api_key:
    st.error("La clé API Cohere n'est pas définie dans les secrets.")
    st.stop()

co = cohere.Client(cohere_api_key)

# Fonction pour envoyer une requête à Cohere
def envoyer_message_cohere(message):
    # Prompt pour le modèle Cohere
    prompt = (
        "Vous êtes un enseignant qui répond à des parents ayant des préoccupations concernant leurs enfants. "
        "Votre ton doit être rassurant, calme et empathique. Répondez avec bienveillance et patience.\n\n"
        f"Question : {message}\nRéponse :"
    )

    # Appel à l'API Cohere pour générer une réponse
    try:
        response = co.generate(
            model="command-xlarge-nightly",  # Modèle recommandé pour la génération de texte
            prompt=prompt,
            max_tokens=150,  # Limiter la taille de la réponse
            temperature=0.7  # Contrôle de la créativité de la réponse
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"Une erreur s'est produite lors de la génération de la réponse : {e}"

# Interface Streamlit
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
st.image("https://images.unsplash.com/photo-1503676260728-1c00da094a0b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDEwfGVkdWNhdGlvbnxlbnwwfHx8fDE2NDk1Nzc3NjI&ixlib=rb-1.2.1&q=80&w=1080", use_container_width=True)

# Interface Streamlit
st.title("Assistant ASH pour les parents")

st.markdown("""
Je suis votre assistant, conçu pour vous aider à naviguer à travers les questions et préoccupations concernant les situations des élèves à besoins particuliers. Mon objectif est de vous fournir des informations claires et rassurantes.
N'hésitez pas à poser vos questions : je suis là pour vous écouter et vous soutenir à chaque étape de votre parcours. Que ce soit pour des conseils, des informations sur les procédures ou des ressources, je suis ici pour vous aider !
""")

# Initialisation de l'historique de la conversation
if 'historique' not in st.session_state:
    st.session_state['historique'] = []

# Texte d'entrée pour poser une question
message = st.text_input("Poser vos questions:")

if st.button("Envoyer"):
    if message:
        # Ajouter le message de l'utilisateur à l'historique
        st.session_state['historique'].append({"role": "user", "message": message})
        
        # Envoyer la requête à Cohere pour obtenir une réponse
        reponse = envoyer_message_cohere(message)
        
        # Ajouter la réponse de l'assistant à l'historique
        st.session_state['historique'].append({"role": "bot", "message": reponse})

# Afficher l'historique de la conversation
for message in st.session_state['historique']:
    if message['role'] == 'user':
        st.write(f"**Moi:** {message['message']}")
    else:
        st.write(f"**Assistant ASH:** {message['message']}")