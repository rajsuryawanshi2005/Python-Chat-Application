import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5556

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def receive():
    while True:
        try:
            message = client.recv(1024).decode()

            if message == "NICK":
                client.send(nickname.encode())

            else:
                print(message)

        except Exception as error:
            print("Error:", error)
            client.close()
            break


def write():
    while True:
        text = input("")
        current_time = datetime.now().strftime("%H:%M:%S")

        if text.startswith("/msg"):
            message = text
        else:
            message = f"[{current_time}] {nickname}: {text}"

        client.send(message.encode())


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
