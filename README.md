# Chatbot Project

This project consists of two main parts: a **FastAPI backend** that hosts a conversational AI, and a **React frontend** that provides a user interface for interacting with the chatbot.

## Table of Contents

1.  [Features](https://www.google.com/search?q=%23features)
2.  [Prerequisites](https://www.google.com/search?q=%23prerequisites)
3.  [Project Structure](https://www.google.com/search?q=%23project-structure)
4.  [Backend Setup (FastAPI)](https://www.google.com/search?q=%23backend-setup-fastapi)
      * [Installation](https://www.google.com/search?q=%23installation)
      * [Running the Backend](https://www.google.com/search?q=%23running-the-backend)
      * [API Endpoints](https://www.google.com/search?q=%23api-endpoints)
5.  [Frontend Setup (React)](https://www.google.com/search?q=%23frontend-setup-react)
      * [Installation](https://www.google.com/search?q=%23installation-1)
      * [Running the Frontend](https://www.google.com/search?q=%23running-the-frontend)
6.  [Usage](https://www.google.com/search?q=%23usage)
7.  [Troubleshooting](https://www.google.com/search?q=%23troubleshooting)
8.  [Acknowledgements](https://www.google.com/search?q=%23acknowledgements)
9.  [License](https://www.google.com/search?q=%23license)

## 1\. Features

  * **FastAPI Backend:**
      * Serves a chatbot API powered by `chatbot_core` logic.
      * Uses FAISS for efficient similarity search with embeddings.
      * Handles conversational responses based on a CSV knowledge base.
      * CORS enabled for seamless frontend integration.
  * **React Frontend:**
      * Intuitive user interface for sending messages to the chatbot.
      * Displays conversational flow.

## 2\. Prerequisites

Before you begin, ensure you have the following installed on your machine:

  * **Python 3.8+**: For the FastAPI backend.
      * [Download Python](https://www.python.org/downloads/)
  * **Node.js (LTS version)**: For the React frontend. This includes `npm` (Node Package Manager).
      * [Download Node.js](https://nodejs.org/en/download/)
  * **Git (Optional but recommended)**: For cloning the repository.
      * [Download Git](https://git-scm.com/downloads)

## 3\. Project Structure

Assuming your project has a structure similar to this:

```
chatbot-project/
├── backend/
│   ├── main.py             # Your FastAPI application
│   ├── requirements.txt    # Python dependencies
│   ├── chatbot_core.py     # Contains ChatbotCore class and logic
│   └── data/
│       ├── cloud_services_faq.csv  # Your FAQ data
│       └── embeddings_faq.npy      # Pre-computed embeddings
│   └── ... (other backend files)
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   │   └── ... (your React components like ChatInterface.js)
│   ├── package.json        # Node.js/React dependencies
│   └── ... (other frontend files)
├── README.md               # This file
└── .gitignore
```

## 4\. Backend Setup (FastAPI)

Navigate to the `backend` directory to set up the API.

### Installation

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <your-repository-url>
    cd chatbot-project
    ```
2.  **Navigate into the `backend` directory:**
    ```bash
    cd backend
    ```
3.  **Create a Python virtual environment (highly recommended):**
    ```bash
    python -m venv venv
    ```
4.  **Activate the virtual environment:**
      * **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
      * **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
5.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```
      * **Note:** Ensure your `requirements.txt` is updated with the correct dependencies, especially if `chatbot_core.py` has specific machine learning libraries. It should look like this:
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

### Running the Backend

Once all dependencies are installed, you can start the FastAPI server:

```bash
uvicorn main:app --reload --port 8500
```

  * `main`: Refers to your `main.py` file. If your FastAPI app is in a different file (e.g., `app.py`), change `main` to `app`.
  * `app`: Refers to the FastAPI application instance (e.g., `app = FastAPI()`).
  * `--reload`: Automatically reloads the server on code changes (useful for development).
  * `--port 8500`: Specifies the port for the server.

You should see output indicating the server is running, typically on `http://127.0.0.1:8500`.
You can verify the API is running by visiting the Swagger UI: `http://127.0.0.1:8500/docs`

### API Endpoints

  * **`POST /chat`**:
      * **Description:** Sends a user message to the chatbot and receives a response.
      * **Request Body (JSON):**
        ```json
        {
          "message": "string"
        }
        ```
      * **Response (JSON):**
        ```json
        {
          "response": "string"
        }
        ```

## 5\. Frontend Setup (React)

Open a **new terminal window** and navigate to the `frontend` directory to set up the React application.

### Installation

1.  **Navigate into the `frontend` directory:**
    ```bash
    cd ../frontend # If you are in the backend directory
    # OR
    cd chatbot-project/frontend # If you are in the project root
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

1.  Ensure **both** the FastAPI backend (on `http://127.0.0.1:8500`) and the React frontend (on `http://localhost:3000`) are running simultaneously.
2.  Open your browser to `http://localhost:3000`.
3.  Type your message into the input field and press "Send" or Enter.
4.  The chatbot's response will appear in the chat interface.

## 7\. Troubleshooting

  * **"Connection refused" or "Not Found" errors on the frontend:**
      * **Solution:** Ensure your FastAPI backend is running on `http://127.0.0.1:8500`. Check the terminal where you started the backend for any errors.
  * **CORS errors ("Cross-Origin Request Blocked"):**
      * **Solution:** Verify that CORS is correctly configured in your FastAPI `main.py` file to allow requests from `http://localhost:3000`.
        ```python
        from fastapi.middleware.cors import CORSMiddleware

        app = FastAPI()

        origins = [
            "http://localhost",
            "http://localhost:3000",
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
  * **"422 Unprocessable Entity" errors from FastAPI:**
      * **Solution:** This usually means the data sent from your React frontend does not match the `Query` Pydantic model expected by your FastAPI `/chat` endpoint. Ensure your React code sends data in the format `{"message": "your_text_here"}`.
  * **"ModuleNotFoundError" when running the backend:**
      * **Solution:** You're missing a Python dependency. Activate your virtual environment (`source venv/bin/activate` or `.\venv\Scripts\activate`) and run `pip install -r requirements.txt` again. Double-check that all required libraries (especially those used by `chatbot_core.py`) are listed in `requirements.txt`.
  * **`faiss` installation issues:**
      * **Solution:** `faiss` can sometimes be tricky. Ensure you have the correct version (`faiss-cpu` for CPU, `faiss-gpu` for GPU with CUDA). Check FAISS documentation for specific system requirements if problems persist.

## 8\. Acknowledgements

  * [FastAPI](https://fastapi.tiangolo.com/)
  * [React](https://react.dev/)
  * [Uvicorn](https://www.uvicorn.org/)
  * [Pydantic](https://pydantic.dev/)
  * [Pandas](https://pandas.pydata.org/)
  * [NumPy](https://numpy.org/)
  * [FAISS](https://faiss.ai/)
  * [Sentence Transformers](https://www.sbert.net/)

