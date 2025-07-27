# _backend/chatbot_core.py

import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os
import random
import re # Import the regular expression module for cleaning text

class ChatbotCore:
    def __init__(self, csv_path: str, embedding_path: str):
        """
        Initializes the ChatbotCore by loading FAQ data, embeddings,
        and setting up the Sentence Transformer model and FAISS index.

        Args:
            csv_path (str): The full path to the CSV file containing FAQs.
            embedding_path (str): The full path to the .npy file for embeddings.
        """
        self.csv_path = csv_path
        self.embedding_path = embedding_path
        self.df = None
        self.model = None
        self.embeddings = None
        self.index = None

        # --- Define Pre-defined Responses ---
        # These are handled before the semantic search
        self.predefined_responses = {
            "hi": "Hello there! How can I assist you with cloud services today?",
            "hello": "Hi! What can I help you with regarding cloud services?",
            "hey": "Hey! Ask me anything about cloud services.",
            "how are you": "I'm a bot, so I don't have feelings, but I'm ready to help you with cloud services questions!",
            "thank you": "You're welcome! Happy to help.",
            "thanks": "No problem! Let me know if you have more questions.",
            "bye": "Goodbye! Have a great day.",
            "goodbye": "Farewell! Feel free to return if you have more questions.",
            # Add more as needed
        }
        # ------------------------------------

        # Load data and initialize components in order
        self._load_data()
        self._initialize_model()
        self.embeddings = self.load_or_compute_embeddings()
        self._build_faiss_index()

    def _load_data(self):
        """Loads FAQs from CSV into a pandas DataFrame."""
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"FAQs CSV not found at: {self.csv_path}")

        self.df = pd.read_csv(self.csv_path)
        if 'Question' not in self.df.columns or 'Answer' not in self.df.columns:
            raise ValueError("CSV must contain 'Question' and 'Answer' columns.")

        self.df['text'] = self.df['Question'] + ' ' + self.df['Answer']
        print(f"Loaded {len(self.df)} FAQs from {self.csv_path}")

    def _initialize_model(self):
        """Initializes the Sentence Transformer model."""
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        print(f"Initialized SentenceTransformer model: sentence-transformers/all-MiniLM-L6-v2")

    def load_or_compute_embeddings(self) -> np.ndarray:
        """
        Loads embeddings from the .npy file if it exists and is valid,
        otherwise computes them from the FAQ text and saves them.
        """
        try:
            print(f"Attempting to load embeddings from: {self.embedding_path}")
            loaded_embeddings = np.load(self.embedding_path)
            if loaded_embeddings.shape[0] != len(self.df):
                print("Warning: Loaded embeddings count does not match FAQ count. Recomputing embeddings.")
                raise FileNotFoundError
            print("Embeddings loaded successfully.")
            return loaded_embeddings
        except FileNotFoundError:
            print(f"Embeddings file not found or mismatched. Computing new embeddings...")
            if self.df is None or 'text' not in self.df.columns:
                raise ValueError("FAQ DataFrame or 'text' column not available for embedding computation.")

            embeddings = self.model.encode(self.df['text'].tolist(), show_progress_bar=True)
            np.save(self.embedding_path, embeddings)
            print(f"Embeddings computed and saved to: {self.embedding_path}")
            return embeddings
        except Exception as e:
            print(f"Error loading embeddings: {e}. Recomputing embeddings.")
            embeddings = self.model.encode(self.df['text'].tolist(), show_progress_bar=True)
            np.save(self.embedding_path, embeddings)
            print(f"Embeddings computed and saved to: {self.embedding_path}")
            return embeddings

    def _build_faiss_index(self):
        """Builds a FAISS index for efficient similarity search."""
        if self.embeddings is None or self.embeddings.size == 0:
            raise ValueError("Embeddings are empty. Cannot build FAISS index.")

        embedding_dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(embedding_dimension)
        self.index.add(self.embeddings.astype('float32'))
        print(f"FAISS index built with {self.index.ntotal} embeddings.")

    def _normalize_query(self, query: str) -> str:
        """Normalizes the query for matching with predefined responses."""
        query = query.lower() # Convert to lowercase
        query = re.sub(r'[^\w\s]', '', query) # Remove punctuation
        return query.strip() # Remove leading/trailing whitespace

    def get_response(self, user_query: str, L2_DISTANCE_THRESHOLD: float = 0.8) -> str:
        """
        Finds the most similar FAQ to the user's query using FAISS,
        or returns a predefined response for common phrases.

        Args:
            user_query (str): The question asked by the user.
            L2_DISTANCE_THRESHOLD (float): The maximum L2 distance for a match to be considered relevant.

        Returns:
            str: The chatbot's answer or a fallback message.
        """
        if not user_query.strip():
            return "⚠️ Please enter a question."

        # --- 1. Check for Pre-defined Responses ---
        normalized_query = self._normalize_query(user_query)
        for phrase, response in self.predefined_responses.items():
            if phrase in normalized_query:
                print(f"User Query: '{user_query}' -> Predefined Response: '{response}'")
                return response
        # ------------------------------------------

        if self.model is None or self.index is None:
            return "Chatbot core not fully initialized. Please check backend setup."

        # 2. Proceed with FAISS search if no predefined response found
        query_embedding = self.model.encode([user_query]).astype('float32')

        if self.index.ntotal == 0:
            return "⚠️ Embeddings are empty in FAISS index. Please check the FAQ setup."

        distances, indices = self.index.search(query_embedding, k=1)

        best_distance = distances[0][0]
        best_match_idx = indices[0][0]

        if best_distance <= L2_DISTANCE_THRESHOLD:
            matched_question = self.df.iloc[best_match_idx]['Question']
            answer = self.df.iloc[best_match_idx]['Answer']
            print(f"User Query: '{user_query}'")
            print(f"Best Match (L2 Distance: {best_distance:.4f}, Index: {best_match_idx}): '{matched_question}'")
            return answer
        else:
            print(f"No good match found for '{user_query}' (Best L2 Distance: {best_distance:.4f})")
            return "❗ Sorry, this chatbot can only help with cloud services. Please ask something related!"

    def get_random_questions(self, count: int = 6) -> list[str]:
        """
        Returns a list of 'count' random questions from the FAQ dataset.
        """
        if self.df is None or self.df.empty:
            return []
        
        num_questions = len(self.df)
        if count > num_questions:
            count = num_questions

        random_questions = random.sample(self.df['Question'].tolist(), count)
        return random_questions

