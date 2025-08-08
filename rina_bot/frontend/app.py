import sys
import os
import time
import requests
from flask import Flask, render_template, request, redirect, url_for, session
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.database import ConversationDB
from backend.admin_routes import admin_routes

app = Flask(__name__)
app.secret_key = "rina123"

app.register_blueprint(admin_routes)

db = ConversationDB()

FASTAPI_URL = "http://localhost:8000/chat"
PING_URL = "http://localhost:8000/ping"
SESSION_TIMEOUT = 180  # 3 minutes


def clean_latex(text):
    return re.sub(r"\$\\boxed{(.+?)}\$", r"\1", text) \
             .replace("$$", "") \
             .replace("\\(", "") \
             .replace("\\)", "") \
             .replace("\\boxed", "") \
             .replace("$", "")


def check_gemini_status():
    try:
        res = requests.get(PING_URL, timeout=3)
        return res.json().get("status") == "ok"
    except Exception:
        return False


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_id = db.validate_user(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["pending"] = None
            session["last_active"] = time.time()

            session_id = db.get_latest_session(user_id)
            if session_id is None:
                session_id = db.create_session(user_id)
            session["session_id"] = session_id

            if session_id:
                history = db.get_conversation_by_session(session_id)
                session["messages"] = [
                    ("You", q) if i % 2 == 0 else ("RINA", a)
                    for i, (q, a, _) in enumerate(history)]
            else:
                session["messages"] = []

            if username == "admin":
                return redirect(url_for("admin_routes.show_conversations"))

            return redirect(url_for("chat_view"))
        else:
            return render_template("login.html", error="Invalid credentials.")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        success, error = db.create_user(username, password)
        if success:
            return redirect(url_for("login"))
        else:
            return render_template("register.html", error=error)
    return render_template("register.html")


@app.route("/chat", methods=["GET", "POST"])
def chat_view():
    print("SESSION user_id:", session.get("user_id"))

    if "user_id" not in session or session.get("user_id") is None:
        return redirect(url_for("login"))

    if time.time() - session.get("last_active", 0) > SESSION_TIMEOUT:
        session.clear()
        return redirect(url_for("login"))

    session["last_active"] = time.time()

    user_id = session.get("user_id")
    session_id = session.get("session_id")
    if not session_id:
        print("ℹsession_id lipsa, il creez acum.")
        session_id = db.create_session(user_id)
        session["session_id"] = session_id
        session["messages"] = []
    messages = session.get("messages", [])
    pending = session.get("pending")

    print(" SESSION DEBUG:", dict(session))

    if request.method == "POST":
        rate_value = request.form.get("rate")

        if rate_value == "good" and pending:
            if not user_id or not session_id:
                print("user_id sau session_id lipsa la salvare pending")
                return redirect(url_for("login"))
            messages.append(("You", pending[0]))
            messages.append(("RINA", pending[1]))
            db.save(user_id, pending[0], pending[1], session_id)
            session["pending"] = None
            session["messages"] = messages
            return redirect(url_for("chat_view"))

        elif rate_value == "bad":
            session["pending"] = None
            return redirect(url_for("chat_view"))

        elif "message" in request.form:
            user_msg = request.form["message"]

            if session.get("messages") and session["messages"][-1][0] == "You" and session["messages"][-1][1] == user_msg:
                print("Mesaj repetat, ignorat.")
                return redirect(url_for("chat_view"))

            if not user_id:
                print("EROARE: user_id lipsa la trimiterea mesajului.")
                return redirect(url_for("login"))

            try:
                res = requests.post(FASTAPI_URL, json={
                    "message": user_msg,
                    "user_id": user_id
                })

                bot_reply = res.json().get("response", "[No response]")
                bot_reply = clean_latex(bot_reply)
            except Exception as e:
                bot_reply = f"[Error contacting backend: {e}]"

            session["pending"] = (user_msg, bot_reply)
            return redirect(url_for("chat_view"))

    gemini_ok = check_gemini_status()
    sessions = db.get_sessions(user_id)
    return render_template("chat.html", messages=messages, pending=pending, gemini_ok=gemini_ok, sessions=sessions)


@app.route("/new_chat")
def new_chat():
    if "user_id" not in session:
        return redirect(url_for("login"))
    session_id = db.create_session(session["user_id"])
    session["session_id"] = session_id
    session["messages"] = []
    session["pending"] = None
    return redirect(url_for("chat_view"))


@app.route("/session/<int:session_id>")
def load_session(session_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    session["session_id"] = session_id
    history = db.get_conversation_by_session(session_id)
    session["messages"] = [("You", q) if i % 2 == 0 else ("RINA", a)
                           for i, (q, a, _) in enumerate(history)]
    return redirect(url_for("chat_view"))


@app.route("/rename_session/<int:session_id>", methods=["POST"])
def rename_session(session_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    new_title = request.form.get("new_title", "").strip()
    if new_title:
        db.rename_session(session_id, new_title)
    return redirect(url_for("chat_view"))


@app.route("/delete_session/<int:session_id>", methods=["POST"])
def delete_session(session_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    db.delete_session(session_id)
    if session.get("session_id") == session_id:
        session["session_id"] = None
        session["messages"] = []
    return redirect(url_for("chat_view"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
