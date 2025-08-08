import sqlite3

db_path = (r"C:\Users\lyang\OneDrive - ENDAVA\Teme\Py\rina_bot\conversations.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(conversations)")
columns = [col[1] for col in cursor.fetchall()]

if "session_id" not in columns:
    cursor.execute("ALTER TABLE conversations ADD COLUMN session_id INTEGER")
    conn.commit()
    print(" Adăugat: session_id în conversations.")
else:
    print("ℹ Coloana session_id deja există.")

conn.close()
