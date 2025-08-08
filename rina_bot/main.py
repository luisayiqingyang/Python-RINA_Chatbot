# main.py

from core.auth import Authenticator
from core.chatbot import ChatBot


def main():
    auth = Authenticator(correct_password="admin123")
    if not auth.login():
        print("Incorrect password. Access denied.")
        return

    print("Login successful. You can start chatting with RINA.")
    print("Type 'exit' to quit.\n")

    chatbot = ChatBot()
    try:
        while True:
            user_input = input("You> ")
            if user_input.lower() == "exit":
                break
            response = chatbot.ask(user_input)
            print("RINA>", response)
    finally:
        chatbot.close()


if __name__ == "__main__":
    main()
