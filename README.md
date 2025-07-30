# Chatbot Project Documentation

This project consists of two main parts: a **FastAPI backend** that hosts a conversational AI, and a **React frontend** that provides an intuitive user interface for interacting with the chatbot. The chatbot is specifically designed to help users learn more about **cloud services**, including how they work and their technical aspects, drawing information from a predefined knowledge base.

## Table of Contents

1.  Features
2.  Prerequisites
3.  Project Structure
4.  Backend Setup (FastAPI)
    * Installation
    * Running the Backend
    * API Endpoints
5.  Frontend Setup (React)
    * Installation
    * Running the Frontend
6.  Usage
7.  Troubleshooting
8.  Acknowledgements

## 1. Features

* **FastAPI Backend:**
    * Serves a chatbot API powered by `chatbot_core.py` logic.
    * Uses FAISS for efficient similarity search with embeddings.
    * Handles conversational responses based on a CSV knowledge base (`cloud_services_faq.csv`).
    * Predefined responses for common greetings and farewells.
    * Ability to suggest random questions from the knowledge base.
    * CORS enabled for seamless frontend integration.
* **React Frontend:**
    * Intuitive user interface for sending messages to the chatbot.
    * Displays conversational flow in a chat bubble format.
    * Designed using React.js for a responsive and dynamic user experience.
    * Can display suggested random questions, enhancing user interaction.

## 2. Prerequisites

Before you begin, ensure you have the following installed on your machine:

* **Python 3.8+**: For the FastAPI backend.
    * [Download Python](https://www.python.org/downloads/)
* **Node.js (LTS version)**: For the React frontend. This includes `npm` (Node Package Manager).
    * [Download Node.js](https://nodejs.org/en/download/)
* **Git (Optional but recommended)**: For cloning the repository.
    * [Download Git](https://git-scm.com/downloads)

## 3. Project Structure

The project is organized into two main directories: `backend` for the FastAPI application and `frontend/chatbot-app` for the React application.

```

.
├── backend/
│   ├── data/
│   │   ├── cloud\_services\_faq.csv    \# The knowledge base for the chatbot (Questions and Answers)
│   │   └── embeddings\_faq.npy        \# Pre-computed embeddings of the FAQ data (generated on first run)
│   ├── **init**.py                 \# Makes 'backend' a Python package (important for imports)
│   ├── chatbot\_api.py              \# The main FastAPI application, exposing chatbot endpoints
│   └── chatbot\_core.py             \# Contains the core conversational AI logic (embedding, FAISS search, response generation)
│   └── requirements.txt            \# Python dependencies for the backend
├── frontend/
│   └── chatbot-app/
│       ├── public/                 \# Static assets for the React app
│       ├── src/                    \# React source code (components, logic, etc.)
│       │   ├── App.js              \# Main React component
│       │   ├── CloudBackground.js  \#displays clickable, floating "clouds" with random questions fetched from the backend.
            └── ...
│       ├── .gitignore
│       ├── package.json            \# Node.js dependencies and project metadata for the React app
│       ├── package-lock.json       \# Records the exact versions of dependencies
│       └── README.md               \# Frontend-specific README (can be combined into top-level)
├── .gitignore                      \# Git ignore file for the entire project
└── README.md                       \# This overall project README file

````

## 4. Backend Setup (FastAPI)

Navigate to the `backend` directory to set up the API.

### Installation

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone [https://github.com/SaraNizarKhayat/cloud-services-chatbot.git](https://github.com/SaraNizarKhayat/cloud-services-chatbot.git)
    cd cloud-services-chatbot
    ```
2.  **Navigate into the `backend` directory:**
    ```bash
    cd backend
    ```
3.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```
    * **Note:** Ensure your `requirements.txt` is updated with the correct dependencies.
        ```
        fastapi==0.111.0
        uvicorn==0.30.1
        pydantic==2.8.2
        python-multipart==0.0.9
        pandas==2.2.2
        numpy==1.26.4
        faiss-cpu==1.8.0 # Or faiss-gpu if you have a GPU
        sentence-transformers==2.7.0
        ```
    * **Data Preparation**: Ensure you have `cloud_services_faq.csv` populated with your cloud service questions and answers inside the `backend/data/` directory. The `embeddings_faq.npy` file will be automatically generated upon the first run of the `ChatbotCore` if it doesn't exist or is outdated.

### Running the Backend

Once all dependencies are installed, you can start the FastAPI server:

```bash
python -m uvicorn chatbot_api:app --host 127.0.0.1 --port 8000 --reload
````

You should see output indicating the server is running, typically on `http://127.0.0.1:8000`.
You can verify the API is running by visiting the Swagger UI: `http://127.0.0.1:8000/docs`

### API Endpoints

The FastAPI backend exposes the following endpoints:

  * **`GET /`**:

      * **Description:** A simple health check endpoint to verify if the API is running and the `ChatbotCore` is initialized.
      * **Response (JSON):**
        ```json
        {
          "message": "Chatbot API is running and core is initialized!"
        }
        ```
        or a 500 error if `ChatbotCore` failed to initialize.

  * **`POST /chat`**:

      * **Description:** Sends a user message to the chatbot and receives an intelligent response based on the knowledge base or predefined rules.
      * **Request Body (JSON):**
        ```json
        {
          "user_message": "string"
        }
        ```
      * **Response (JSON):**
        ```json
        {
          "response": "string"
        }
        ```

  * **`GET /random_questions`**:

      * **Description:** Fetches a list of random questions from the loaded FAQ knowledge base. Useful for populating suggested questions in the frontend.
      * **Query Parameters:**
          * `count` (integer, optional): The number of random questions to return. Defaults to `6`.
      * **Response (JSON):**
        ```json
        {
          "questions": ["string", "string", ...]
        }
        ```

### Backend Logic (`chatbot_core.py` and `chatbot_api.py` in detail)

#### `backend/chatbot_core.py`

This file encapsulates the core intelligence of the chatbot.

  * **Class `ChatbotCore`**:
      * **`__init__(self, csv_path: str, embedding_path: str)`**:
          * Initializes the chatbot with paths to the FAQ CSV and embedding file.
          * Loads the knowledge base (`_load_data`), initializes the `SentenceTransformer` model (`_initialize_model`), loads or computes question embeddings (`load_or_compute_embeddings`), and builds the FAISS index (`_build_faiss_index`) upon instantiation.
          * Defines a dictionary of `predefined_responses` for common greetings and farewells (e.g., "hi", "thank you").
      * **`_load_data(self)`**:
          * Reads the `cloud_services_faq.csv` file into a Pandas DataFrame.
          * Ensures the CSV contains 'Question' and 'Answer' columns.
          * Combines 'Question' and 'Answer' into a 'text' column for embedding.
      * **`_initialize_model(self)`**:
          * Loads the `sentence-transformers/all-MiniLM-L6-v2` model, which is used to convert text (questions and user queries) into numerical vector embeddings.
      * **`load_or_compute_embeddings(self) -> np.ndarray`**:
          * Checks if pre-computed embeddings (`embeddings_faq.npy`) exist and are valid (i.e., match the number of FAQs).
          * If valid, loads them directly.
          * Otherwise, computes new embeddings from the FAQ text using the `SentenceTransformer` model and saves them to the `.npy` file for future use, preventing redundant computation.
      * **`_build_faiss_index(self)`**:
          * Initializes a FAISS `IndexFlatL2` (a simple L2 distance-based index) using the dimension of the embeddings.
          * Adds all computed FAQ embeddings to the FAISS index, enabling fast similarity searches.
      * **`_normalize_query(self, query: str) -> str`**:
          * A helper method to clean and standardize user input by converting it to lowercase and removing punctuation, aiding in matching with predefined responses.
      * **`get_response(self, user_query: str, L2_DISTANCE_THRESHOLD: float = 0.8) -> str`**:
          * The main method for generating chatbot responses.
          * First, it checks for empty queries.
          * It then attempts to match the `normalized_query` against `predefined_responses`.
          * If no predefined match, it encodes the `user_query` into an embedding.
          * Performs a similarity search using the FAISS index to find the most similar FAQ question.
          * If the `L2_DISTANCE_THRESHOLD` is met (meaning a good enough match is found), it returns the corresponding answer from the FAQ.
          * Otherwise, it returns a generic "out of scope" message.
      * **`get_random_questions(self, count: int = 6) -> list[str]`**:
          * Returns a specified `count` of random questions from the loaded FAQ dataset. Useful for initializing the chat or providing user prompts.

#### `backend/chatbot_api.py`

This file sets up the FastAPI application to serve the `ChatbotCore` logic as an API.

  * **FastAPI Initialization**:
      * `app = FastAPI()`: Creates the FastAPI application instance.
  * **CORS Configuration**:
      * Sets up `CORSMiddleware` to allow requests from the React frontend (`http://localhost:3000`), preventing cross-origin security issues. `allow_origins`, `allow_credentials`, `allow_methods`, and `allow_headers` are configured to allow flexible communication during development.
  * **ChatbotCore Initialization**:
      * Initializes `chatbot_instance = ChatbotCore(...)` globally when the API starts. This loads all necessary data and models once, making subsequent API calls fast.
      * Includes robust error handling during initialization to provide informative messages if the CSV or embeddings files are not found or if there are other setup issues.
  * **Pydantic Model `ChatRequest`**:
      * Defines the expected structure for incoming JSON requests to the `/chat` endpoint, ensuring that a `user_message` string is always present.
  * **API Endpoints (`@app.get` and `@app.post`)**:
      * `@app.get("/")`: A simple root endpoint to check if the API is alive and if `ChatbotCore` has been successfully initialized.
      * `@app.post("/chat")`: The primary endpoint for chatbot interaction. It receives a `ChatRequest`, passes the `user_message` to `chatbot_instance.get_response()`, and returns the bot's reply.
      * `@app.get("/random_questions")`: An endpoint to fetch random questions from the knowledge base, often used by the frontend to suggest conversation starters.
  * **Uvicorn Runner (`if __name__ == "__main__":`)**:
      * Allows running the API directly using `python chatbot_api.py`, though `uvicorn chatbot_api:app` is the recommended way for production-like environments as it offers more control.

## 5\. Frontend Setup (React)

Open a **new terminal window** and navigate to the `frontend/chatbot-app` directory to set up the React application.

### Installation

1.  **Navigate into the `frontend/chatbot-app` directory:**
    ```bash
    cd frontend/chatbot-app
    ```
2.  **Install the Node.js dependencies:**
    ```bash
    npm install
    # OR if you prefer Yarn:
    # yarn install
    ```

### Running the Frontend

After installing the dependencies, you can start the React development server:

```bash
npm start
# OR
# yarn start
```

This will typically open your React application in your browser at `http://localhost:3000`.

## 6\. Usage

1.  Ensure **both** the FastAPI backend (on `http://127.0.0.1:8000`) and the React frontend (on `http://localhost:3000`) are running simultaneously.
      * Open one terminal for the backend: `cd backend && uvicorn chatbot_api:app --host 127.0.0.1 --port 8000 --reload`
      * Open another terminal for the frontend: `cd frontend/chatbot-app && npm start`
2.  Open your browser to `http://localhost:3000`.
3.  Type your message into the input field and press "Send" or Enter.
4.  The chatbot's response will appear in the chat interface. You can also click on the suggested random questions to quickly get answers.

## 7\. Troubleshooting

  * **"Connection refused" or "Not Found" errors on the frontend:**
      * **Solution:** Ensure your FastAPI backend is running on `http://127.0.0.1:8000`. Check the terminal where you started the backend for any errors.
  * **CORS errors ("Cross-Origin Request Blocked"):**
      * **Solution:** Verify that CORS is correctly configured in your FastAPI `chatbot_api.py` file to allow requests from `http://localhost:3000`. The configuration provided in `chatbot_api.py` should work, but double-check if you've made any modifications.
        ```python
        from fastapi.middleware.cors import CORSMiddleware

        app = FastAPI()

        origins = [
            "http://localhost:3000",
            "[http://127.0.0.1:3000](http://127.0.0.1:3000)",
        ]

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        ```
      * **Remember to restart your FastAPI server after making CORS changes.**
  * **"ModuleNotFoundError" when running the backend:**
      * **Solution:** You're missing a Python dependency. Activate your virtual environment (if using one) and run `pip install -r requirements.txt` again from the `backend` directory. Double-check that all required libraries (especially `faiss-cpu`, `sentence-transformers`, `pandas`, `numpy`) are listed in `requirements.txt`.
  * **`faiss` installation issues:**
      * **Solution:** `faiss` can sometimes be tricky. Ensure you have the correct version (`faiss-cpu` for CPU, `faiss-gpu` for GPU with CUDA). Check FAISS documentation for specific system requirements if problems persist. If you encounter issues, try uninstalling and reinstalling `faiss-cpu` specifically: `pip uninstall faiss-cpu && pip install faiss-cpu`.
  * **`embeddings_faq.npy` not found or not generating:**
      * **Solution:** Ensure `cloud_services_faq.csv` exists and is correctly populated in `backend/data/`. The `ChatbotCore` will attempt to generate `embeddings_faq.npy` on its first run if it's missing or corrupted. Check the backend terminal for error messages during `ChatbotCore` initialization. Ensure the `data` directory is correctly located relative to `chatbot_api.py` (as shown in the `Project Structure`).

## 8\. Acknowledgements

  * [FastAPI](https://fastapi.tiangolo.com/)
  * [React](https://react.dev/)
  * [Uvicorn](https://www.uvicorn.org/)
  * [Pydantic](https://pydantic.dev/)
  * [Pandas](https://pandas.pydata.org/)
  * [NumPy](https://numpy.org/)
  * [FAISS](https://faiss.ai/)
  * [Sentence Transformers](https://www.sbert.net/)
