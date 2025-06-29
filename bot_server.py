import os
import sqlite3
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key="AIzaSyA8lEE41kySADz3gHHPZwUvD40xgS5gQxQ")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# ───── Flask setup ─────
app = Flask(__name__, static_folder=".")
CORS(app)

# ───── Load docs ─────
DOC_FILE = "hyperrcompute_docs.txt"
hyperr_docs = "hyperrcompute_docs.txt not found."
if os.path.exists(DOC_FILE):
    with open(DOC_FILE, "r", encoding="utf-8") as f:
        hyperr_docs = f.read()

# ───── SQLite setup ─────
DB_FILE = "chat.db"
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    created_at TEXT
)''')
c.execute('''CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    role TEXT,
    content TEXT,
    timestamp TEXT
)''')
conn.commit()

# ───── Routes ─────
@app.route("/")
def home():
    return send_from_directory(".", "chat.html")

@app.route("/sessions")
def get_sessions():
    c.execute("SELECT id, created_at FROM sessions ORDER BY created_at DESC")
    return jsonify([{"id": row[0], "created_at": row[1]} for row in c.fetchall()])

@app.route("/new_session", methods=["POST"])
def new_session():
    session_id = str(uuid.uuid4())
    created_at = datetime.now().isoformat()
    c.execute("INSERT INTO sessions (id, created_at) VALUES (?, ?)", (session_id, created_at))
    conn.commit()
    return jsonify({"id": session_id, "created_at": created_at})

@app.route("/chat/<session_id>")
def get_chat(session_id):
    c.execute("SELECT role, content, timestamp FROM messages WHERE session_id = ? ORDER BY id", (session_id,))
    return jsonify([{"role": row[0], "content": row[1], "timestamp": row[2]} for row in c.fetchall()])

@app.route("/session/<session_id>", methods=["DELETE"])
def delete_session(session_id):
    c.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    c.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    conn.commit()
    return jsonify({"status": "deleted"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    session_id = data.get("session_id")
    user_message = data.get("message", "").strip()

    timestamp = datetime.now().isoformat()
    c.execute("INSERT INTO messages (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
              (session_id, "user", user_message, timestamp))
    conn.commit()

    # Load full chat history
    c.execute("SELECT role, content FROM messages WHERE session_id = ? ORDER BY id", (session_id,))
    history = c.fetchall()

    # Format messages for model
    history_text = "\n".join([f"{role.capitalize()}: {content}" for role, content in history])

    system_prompt = f"""
You are Hyperr-Assistant, a technical expert on the decentralized GPU platform HyperrCompute.

Behaviors:
- Adaptively include or skip headings like 'Steps' or 'Docs' based on query.
- NEVER use headings for small talk (e.g., 'hey', 'hello').
- Ask follow-up questions if user asks for estimates without full info.
- Format code/commands in triple backticks for UI copy buttons.
- Always be helpful, brief, and assume user wants direct assistance.

Pricing:
- RTX 4090: 50 sats/minute

Documentation:
{hyperr_docs}

Chat history:
{history_text}
    """

    try:
        response = model.generate_content(system_prompt)
        bot_reply = response.text.strip()
    except Exception as e:
        bot_reply = f"\u274c Error: {str(e)}"

    bot_time = datetime.now().isoformat()
    c.execute("INSERT INTO messages (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
              (session_id, "bot", bot_reply, bot_time))
    conn.commit()

    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

