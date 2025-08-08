from google.cloud import firestore

db = firestore.Client()

def save_message(user_id, session_id, message, response, timestamp):
    doc_ref = db.collection("conversations").document()
    doc_ref.set({
        "user_id": user_id,
        "session_id": session_id,
        "message": message,
        "response": response,
        "timestamp": timestamp,
    })

def get_user_conversations(user_id):
    return db.collection("conversations").where("user_id", "==", user_id).stream()
