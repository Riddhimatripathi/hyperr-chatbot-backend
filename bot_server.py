import os
import sqlite3
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import google.generativeai as genai
import PyPDF2
import docx

# ───── Load environment and API key ─────
load_dotenv()
genai.configure(api_key="AIzaSyA8lEE41kySADz3gHHPZwUvD40xgS5gQxQ")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# ───── Flask app setup ─────
app = Flask(__name__, static_folder=".")
CORS(app)

# ───── Load documentation file ─────
DOC_FILE = "hyperrcompute_docs.txt"
hyperr_docs = ""
if os.path.exists(DOC_FILE):
    with open(DOC_FILE, "r", encoding="utf-8") as f:
        hyperr_docs = f.read()

# ───── SQLite database setup ─────
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

# ───── Upload folder ─────
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ───── Routes ─────

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

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

@app.route("/upload/<session_id>", methods=["POST"])
def upload_file(session_id):
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        ext = os.path.splitext(filename)[1].lower()
        content = ""

        if ext == ".txt":
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        elif ext == ".pdf":
            reader = PyPDF2.PdfReader(filepath)
            content = "\n".join(page.extract_text() or "" for page in reader.pages)
        elif ext == ".docx":
            doc = docx.Document(filepath)
            content = "\n".join(p.text for p in doc.paragraphs)
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        timestamp = datetime.now().isoformat()
        content_msg = f"[Document Uploaded: {filename}]\n\n{content[:4000]}"
        c.execute("INSERT INTO messages (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
                  (session_id, "system", content_msg, timestamp))
        conn.commit()

        return jsonify({"status": "uploaded", "filename": filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    session_id = data.get("session_id")
    user_message = data.get("message", "").strip()
    timestamp = datetime.now().isoformat()

    # Store user message
    c.execute("INSERT INTO messages (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
              (session_id, "user", user_message, timestamp))
    conn.commit()

    # Fetch full session history
    c.execute("SELECT role, content FROM messages WHERE session_id = ? ORDER BY id", (session_id,))
    history = c.fetchall()

    user_history = "\n".join(f"{r.upper()}: {c}" for r, c in history if r in ("user", "bot"))
    uploaded_docs = "\n\n".join(c for r, c in history if r == "system")

    # System prompt
    system_prompt = f"""
You are Hyperr‑Assistant, a technical expert of the decentralized GPU platform HyperrCompute.

📄 Uploaded docs:
{uploaded_docs}

📚 Official Docs:
{hyperr_docs}

💬 Conversation so far:
{user_history}

👤 User's next message:
{user_message}
"""

    try:
        response = model.generate_content(system_prompt)
        bot_reply = response.text.strip()
    except Exception as e:
        bot_reply = f"❌ Error: {str(e)}"

    bot_time = datetime.now().isoformat()
    c.execute("INSERT INTO messages (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
              (session_id, "bot", bot_reply, bot_time))
    conn.commit()

    return jsonify({"response": bot_reply})

# ───── Run app ─────
if __name__ == "__main__":
    app.run(debug=True)
