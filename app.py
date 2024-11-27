import streamlit as st
import openai

# Récupérer la clé API depuis les secrets Streamlit Cloud
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Vérifier si la clé API est présente
if openai.api_key is None:
    st.error("La clé API OpenAI n'est pas définie dans les secrets.")
    st.stop()  # Arrêter l'exécution si la clé API est absente

# Fonction pour envoyer la requête à OpenAI et obtenir la réponse
def envoyer_message_openai(message):
    # Définir le prompt pour donner un ton rassurant et empathique
    prompt = f"""
    Vous êtes un enseignant qui répond à des parents ayant des préoccupations concernant leurs enfants. Votre ton doit être rassurant, calme et empathique. Vous devez répondre aux questions des parents avec bienveillance et patience.
    Question : {message}
    Réponse :
    """

    # Appel à l'API OpenAI pour générer la réponse
    response = openai.Completion.create(
        model="gpt-3.5-turbo",  # Ou gpt-4 si tu utilises cette version
        prompt=prompt,
        temperature=0.7,  # Ton modéré, rassurant
        max_tokens=600,   # Limite de la longueur de la réponse
    )
    
    # Retourner la réponse générée
    return response.choices[0].text.strip()

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

if 'historique' not in st.session_state:
    st.session_state['historique'] = []

# Texte d'entrée pour poser une question
message = st.text_input("Poser vos questions:")

if st.button("Envoyer"):
    if message:
        # Ajouter le message de l'utilisateur à l'historique
        st.session_state['historique'].append({"role": "user", "message": message})
        
        # Envoyer la requête à OpenAI pour obtenir la réponse
        reponse = envoyer_message_openai(message)
        
        # Ajouter la réponse du chatbot à l'historique
        st.session_state['historique'].append({"role": "bot", "message": reponse})

# Afficher l'historique de la conversation
for message in st.session_state['historique']:
    if message['role'] == 'user':
        st.write(f"**Moi:** {message['message']}")
    else:
        st.write(f"**Assistant ASH:** {message['message']}")
