from flask import Blueprint, render_template, request
import sqlite3
import os

admin_routes = Blueprint('admin_routes', __name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "conversations.db")


@admin_routes.route("/conversations")
def show_conversations():
    sort_by = request.args.get("sort_by", "timestamp")
    order = request.args.get("order", "desc")
    user_filter = request.args.get("user_id")

    if sort_by not in ["timestamp", "user_id"]:
        sort_by = "timestamp"
    if order not in ["asc", "desc"]:
        order = "desc"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if user_filter and user_filter.isdigit():
        query = f"""
            SELECT id, user_id, session_id, question, answer, timestamp
            FROM conversations
            WHERE user_id = ?
            ORDER BY {sort_by} {order.upper()}
        """
        cursor.execute(query, (int(user_filter),))
    else:
        query = f"""
            SELECT id, user_id, session_id, question, answer, timestamp
            FROM conversations
            ORDER BY {sort_by} {order.upper()}
        """
        cursor.execute(query)

    rows = cursor.fetchall()
    conn.close()
    return render_template("conversations.html", conversations=rows,
                           sort_by=sort_by, order=order, user_filter=user_filter or "")
