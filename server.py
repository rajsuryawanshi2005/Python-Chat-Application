import socket
import threading

HOST = "127.0.0.1"
PORT = 5556

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def send_users():
    users = ", ".join(nicknames)
    broadcast(f"Online Users: {users}".encode())


def handle(client):
    while True:
        try:
            message = client.recv(1024).decode()

            # Private message feature
            if message.startswith("/msg"):
                parts = message.split(" ", 2)

                if len(parts) >= 3:
                    target_name = parts[1]
                    private_message = parts[2]

                    if target_name in nicknames:
                        index = nicknames.index(target_name)
                        target_client = clients[index]

                        target_client.send(
                            f"[PRIVATE] {private_message}".encode()
                        )
                    else:
                        client.send("User not found".encode())

            else:
                broadcast(message.encode())

        except Exception as error:
            print("Error:", error)

            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()

                nickname = nicknames[index]
                nicknames.remove(nickname)

                broadcast(f"{nickname} left the chat!".encode())
                send_users()

            break


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")

        client.send("NICK".encode())
        nickname = client.recv(1024).decode()

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname is {nickname}")

        broadcast(f"{nickname} joined the chat!".encode())
        send_users()

        client.send("Connected to the server!".encode())

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening...")

receive()
