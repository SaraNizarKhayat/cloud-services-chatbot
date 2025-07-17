import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import faiss
import streamlit as st

# Load data
csv_path = r'C:/Users/sarak/Desktop/project25/Chatbot/data/cloud_services_faq.csv'
df = pd.read_csv(csv_path)
df['text'] = df['Question'] + ' ' + df['Answer']

# Compute embeddings
embedding_path = r'C:/Users/sarak/Desktop/project25/Chatbot/data/embeddings_faq.npy'
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

try:
    embeddings = np.load(embedding_path)
except FileNotFoundError:
    embeddings = model.encode(df['text'].tolist(), show_progress_bar=True)
    np.save(embedding_path, embeddings)

# Build FAISS index
dimension = embeddings.shape[1]
faiss_index = faiss.IndexFlatL2(dimension)
faiss_index.add(embeddings)

# Streamlit UI
st.set_page_config(page_title="Cloud FAQ Chatbot", page_icon="☁️")
st.title("Cloud Services FAQ Chatbot")
st.write("Ask a question related to cloud services and I’ll find the best answer from our FAQ!")

# CSS styling
st.markdown(
    """
    <style>
    /* Set gradient background for the main app */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to bottom, white, #87ceeb);
        color: black;
    }

    /* Optional: also make the main block transparent if needed */
    [data-testid="stAppViewBlockContainer"] {
        background: transparent;
    }

    .chat-container {
        overflow-y: auto;
        max-height: 80vh;
        display: flex;
        flex-direction: column-reverse;
    }

    .chat-bubble {
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        width: fit-content;
        max-width: 80%;
        word-wrap: break-word;
        background-color: white;
        color: black;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .user {
        align-self: flex-end;
        margin-left: auto;
    }

    .bot {
        align-self: flex-start;
        margin-right: auto;
    }
    </style>


    """,
    unsafe_allow_html=True
)

# Session state
if "history" not in st.session_state:
    st.session_state.history = []

# Chatbot logic
def chatbot_response(user_query, threshold=0.6):
    if not user_query.strip():
        return "⚠️ Please enter a question."

    query_embedding = model.encode([user_query])
    similarities = cosine_similarity(query_embedding, embeddings)[0]

    if len(similarities) == 0:
        return "⚠️ Embeddings are empty. Please check the FAQ setup."

    top_idx = similarities.argmax()
    best_score = similarities[top_idx]

    if best_score >= threshold:
        a = df.iloc[top_idx]['Answer']
        return f"{a}"
    else:
        return "❗ Sorry, this chatbot can only help with cloud services. Please ask something related!"

# Append messages to history
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([8, 1])
    with col1:
        user_input = st.text_input("Your question:", key="input", label_visibility="collapsed")
    with col2:
        submit = st.form_submit_button("Send")


if submit and user_input:
    reply = chatbot_response(user_input)
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", reply))

    

# Display chat history
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for speaker, message in reversed(st.session_state.history):
    if speaker == "You":
        bubble_class = "chat-bubble user"
    else:
        bubble_class = "chat-bubble bot"
    st.markdown(f'<div class="{bubble_class}">{speaker}: {message}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
