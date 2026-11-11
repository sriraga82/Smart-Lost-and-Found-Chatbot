# Smart Lost & Found Chatbot

A beginner-friendly Streamlit prototype that guides users through reporting a lost or found item and checks a small set of sample records for possible matches.

## Features
- Chat-style interaction
- Collects item name, colour, and location
- Checks sample found-item records for possible matches
- Adds found-item reports to the current session

## Tech stack
- Python
- Streamlit

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Prototype limitations
This is a rule-based demonstration. Data is stored only in the active Streamlit session and resets when the session restarts. It does not currently use an external LLM, persistent database, RAG/embeddings, or LangGraph. Contact details and ownership verification are intentionally left to the campus lost-and-found desk.
