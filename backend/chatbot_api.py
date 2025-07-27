# _backend/chatbot_api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
import random # Import random for selecting questions

# Import CORSMiddleware for handling cross-origin requests from the frontend
from fastapi.middleware.cors import CORSMiddleware

# Import our ChatbotCore. The dot means "from the current package/directory".
# This requires the 'backend' directory to be recognized as a Python package,
# which is done by having an empty '__init__.py' file inside it.
from chatbot_core import ChatbotCore

# Initialize the FastAPI app
app = FastAPI()

# --- CORS Configuration ---
# List of origins (domains) that are allowed to make requests to your API.
# In development, this will typically be your React app's development server URL.
# In production, this should be your actual frontend domain.
origins = [
    "http://localhost:3000",  # Default port for create-react-app
    "http://127.0.0.1:3000",  # Another common local host address
    # Add other origins if your frontend runs on a different port or domain, e.g.,
    # "http://your-production-domain.com",
]

# Add CORS middleware to the FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Allows specified origins
    allow_credentials=True,         # Allows cookies to be included in cross-origin HTTP requests
    allow_methods=["*"],            # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],            # Allows all headers in the request
)
# --------------------------

# --- Initialize the ChatbotCore instance ---
# This will load data and models when the API starts up.
# We construct absolute paths to ensure files are found regardless of the
# current working directory when the server is started.

# Get the directory of the current script (e.g., 'C:\...\Chatbot\backend')
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to your 'data' directory (without the underscore)
data_dir = os.path.join(current_dir, 'data') # Corrected: 'data' instead of '_data'

# Construct the full paths to your CSV and embeddings files
csv_file_path = os.path.join(data_dir, 'cloud_services_faq.csv')
embeddings_file_path = os.path.join(data_dir, 'embeddings_faq.npy')

# Initialize the ChatbotCore instance.
# It's initialized globally so it's ready for all incoming requests.
chatbot_instance = None # Initialize to None in case of initialization failure
try:
    chatbot_instance = ChatbotCore(csv_path=csv_file_path, embedding_path=embeddings_file_path)
    print("ChatbotCore initialized successfully!")
except Exception as e:
    # Print a detailed error message if initialization fails
    print(f"ERROR: Failed to initialize ChatbotCore: {e}")
    print("Please ensure the following:")
    print(f"  1. '{os.path.basename(csv_file_path)}' exists in '{data_dir}'")
    print(f"  2. '{os.path.basename(embeddings_file_path)}' exists in '{data_dir}' (or will be generated)")
    print("  3. Required Python packages ('faiss-cpu', 'sentence-transformers', 'pandas', 'numpy') are installed.")


# Define the request body model for our chat endpoint.
# This ensures incoming JSON requests have a 'user_message' field.
class ChatRequest(BaseModel):
    user_message: str

# Define a simple GET endpoint for a health check.
# This allows you to verify if the API is running and if ChatbotCore initialized.
@app.get("/")
async def read_root():
    if chatbot_instance:
        return {"message": "Chatbot API is running and core is initialized!"}
    else:
        # If ChatbotCore failed to initialize, return a 500 error.
        raise HTTPException(status_code=500, detail="Chatbot API is running, but core failed to initialize. Check backend logs for details.")

# Define the main POST endpoint for chat interactions.
@app.post("/chat")
async def chat_with_bot(request: ChatRequest):
    """
    Handles incoming user messages, processes them using ChatbotCore,
    and returns the chatbot's response.
    """
    # Ensure ChatbotCore was successfully initialized before processing requests.
    if not chatbot_instance:
        raise HTTPException(status_code=500, detail="Chatbot core not initialized. Cannot process requests.")

    user_message = request.user_message

    # Call the get_response method from our initialized ChatbotCore instance
    bot_response = chatbot_instance.get_response(user_message)

    # Return the bot's response as a JSON object
    return {"response": bot_response}

# New endpoint to provide random questions for the frontend clouds
@app.get("/random_questions")
async def get_random_questions(count: int = 6):
    """
    Returns a list of 'count' random questions from the FAQ dataset.
    """
    if not chatbot_instance:
        raise HTTPException(status_code=500, detail="Chatbot core not initialized. Cannot fetch random questions.")

    questions = chatbot_instance.get_random_questions(count)
    return {"questions": questions}


# This block allows you to run the FastAPI application directly using 'python chatbot_api.py'.
# However, it's generally recommended to use the 'uvicorn' command directly (see instructions below).
if __name__ == "__main__":
    # When running directly, ensure you are in the '_backend' directory
    # or have properly configured your Python path.
    # Uvicorn will look for the 'app' object in this file.
    uvicorn.run(app, host="127.0.0.1", port=8000)

