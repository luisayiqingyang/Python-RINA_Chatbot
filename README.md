
# RINA Bot

RINA Bot is a text-based chatbot developed in Python, using a microservice architecture with FastAPI (for the backend), Flask (for the frontend), and Google Gemini AI for generating responses (LLM integration). The app supports user authentication, conversation logging, asynchronous AI interaction, monitoring, caching and containerization and deployment (Docker and GCP).
<img width="1917" height="1002" alt="login" src="https://github.com/user-attachments/assets/35b04724-b1af-4249-9974-56c6b42da29f" />
<img width="1919" height="997" alt="register" src="https://github.com/user-attachments/assets/19299290-acb2-4dba-b53c-61082fb50192" />

Users can:
- Create new chat sessions (Each session is uniquely saved with a generated title or timestamp, Conversations are stored and retrievable per user).
- Rename chat (Renaming is reflected in the sidebar and history view).
- Delete chat sessions.
<img width="270" height="397" alt="image" src="https://github.com/user-attachments/assets/010453cc-1bef-4752-8951-0e78fb2a49c1" />
																				  
- View their own previous chats.
- Validate answers (for the cache memory):
  <img width="1919" height="997" alt="Screenshot 2025-08-05 103118" src="https://github.com/user-attachments/assets/2c326d8d-5ad8-478a-bf5c-72681bcf4be5" />

- Math questions:
<img width="1917" height="997" alt="Op  mat" src="https://github.com/user-attachments/assets/5229ce6d-a3ce-4a11-b4be-b9acfc32e655" />



Access Control Rules:
- Users only see and manage their own chat history.
- Admin users (username: "admin", pass: "Admin123456789*") can:
           - View all chat sessions across all users.
	   - Filter and sort the entire chat history by date, user ID, timestamp.
<img width="1915" height="1001" alt="Screenshot 2025-08-05 103716" src="https://github.com/user-attachments/assets/c19eb8a6-28f4-4869-8343-d29b1c91d0a1" />


## Tech Stack

Python 
- Used as the core programming language to develop all components—CLI, backend APIs, frontend server, AI integration, and database logic.

FastAPI 
- Used to build the backend API layer that handles chat requests, manages async communication with the Gemini model, and responds to frontend or external API calls.

Flask 
- Used to serve the frontend interface of the chatbot. It provides a lightweight web server where users can interact with RINA through a browser.

Google Gemini AI 
- Used as the AI model to generate intelligent responses. The app connects to Gemini via API calls (async) to handle user input and return natural language replies.

SQLite 
- Used as a lightweight relational database to store user conversations, including questions, responses, timestamps, and session IDs.

Containerization and deployment
- The entire application is containerized using Docker.
- Deployed to Google Cloud Platform (GCP).
- Automatically scales with demand (serverless).
  
Monitoring 
- Monitoring is implemented through a simple health check endpoint (/ping) that sends a test request to Google Gemini API:
If the model responds successfully → a green LED indicates the system is operational
If the response fails or times out → a red LED signals an error or outage

Caching 
- In-memory caching is used via a Python dictionary to store recent user queries and responses, reducing duplicate calls to the Gemini API and improving performance.

Authorization 
- Basic password authentication is implemented in the CLI app. Plans or extensions may include multi-user auth, session tokens, or OAuth for the web version.

Logging 
- A full logging interface is available via the Conversations page, where all user queries and AI responses are displayed with: user_id, session_id, question & AI-generated answer, timestamp, sorting, ordering, and user filtering options.

Pydantic
- Used in the FastAPI backend to validate and serialize request/response data models. Ensures strong typing and guarantees data structure integrity between the client and server.

Flake8
- Static code analysis tool that enforces consistent formatting and detects style violations (PEP8). Helps maintain clean, readable, and maintainable code.

## Project Structure
```text
rina_bot/
├── .dockerignore
├── .flake8                    # Configuration file for flake8, a Python linter enforcing code style and formatting (PEP8).
├── docker-compose.yml         # Defines and runs multi-container Docker applications (e.g., FastAPI + Flask).
├── Dockerfile                 # Instructions for building the Docker image of the application.
├── main.py                    # CLI interface with login and chat
├── run_all.py                 # Runs FastAPI backend and Flask frontend concurrently
├── backend/
│   ├── admin_routes.py
│   ├── api.py                 # FastAPI endpoint for chat communication
│   ├── config.py              # Configuration file (API keys, model names, etc.)
│   ├── conversations.db       # SQLite database for storing chat history
│   └── db.py                  # Functions for saving conversations in SQLite
├── core/
│   ├── ai.py                  # Google Gemini AI client
│   ├── auth.py                # Simple password authentication
│   ├── chatbot.py             # Chat logic (Gemini + DB)
│   ├── database.py            # DB wrapper logic
│   └── firestore_adapter.py   # Firestore-based replacement for SQLite; saves and queries chat data using GCP Firestore
├── frontend/
│   ├── app.py                 # Flask application (web UI)
│   ├── static/
│   │   └── RINA.png           # Logo image for the UI (displayed in the interface).
│   └── templates/
│       ├── chat.html          # The main chat page where users send and receive messages.
│       ├── conversations.html # Displays previous conversation history for the logged-in user.
│       ├── login.html         # Login form template.
│       └── register.html      # Registration form for new users.
└── import_sqlite.py           # A script to import an existing DB into the app.
```

### 1. Install dependencies

Ensure you have Python 3.11+ installed.

```bash
pip install -r requirements.txt
```

### If `requirements.txt` is missing, install manually:

```bash
pip install --no-cache-dir flask fastapi uvicorn google-generativeai aiosqlite bcrypt   google-cloud-firestore google-cloud-secret-manager 

```

### 2. Configure your Gemini API key

```python
GEMINI_API_KEY = "your_api_key_here"
MODEL_NAME = "your_model"
```

### 3. Run the application
The chatbot can be accessed directly at:
https://rina-service-383850703474.europe-west1.run.app/

or

locally using:

```bash
python run_all.py
```

This will launch at: `http://127.0.0.1:8080`







