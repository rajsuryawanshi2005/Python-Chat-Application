import socket
import threading
import tkinter as tk
from tkinter import simpledialog, filedialog

HOST = "127.0.0.1"
PORT = 5556


class ChatClient:

    def __init__(self):

        self.dark_mode = True

        self.window = tk.Tk()
        self.window.title("Python Chat App")
        self.window.geometry("750x550")

        # Ask nickname
        self.nickname = simpledialog.askstring(
            "Nickname", "Enter username:", parent=self.window
        )

        # ===== CHAT AREA =====
        self.chat_canvas = tk.Canvas(self.window, bg="#1e1e1e")
        self.chat_canvas.pack(fill=tk.BOTH, expand=True)

        self.chat_frame = tk.Frame(self.chat_canvas, bg="#1e1e1e")
        self.chat_canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")

        self.chat_frame.bind(
            "<Configure>",
            lambda e: self.chat_canvas.configure(
                scrollregion=self.chat_canvas.bbox("all")
            )
        )

        # ===== INPUT AREA =====
        bottom = tk.Frame(self.window)
        bottom.pack(fill=tk.X)

        self.input_box = tk.Entry(bottom, font=("Arial", 12))
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        send_btn = tk.Button(bottom, text="Send", command=self.send_message)
        send_btn.pack(side=tk.LEFT, padx=5)

        emoji_btn = tk.Button(bottom, text="😊", command=self.open_emoji)
        emoji_btn.pack(side=tk.LEFT)

        file_btn = tk.Button(bottom, text="📎", command=self.send_file)
        file_btn.pack(side=tk.LEFT)

        mode_btn = tk.Button(bottom, text="🌙", command=self.toggle_mode)
        mode_btn.pack(side=tk.LEFT)

        self.window.bind("<Return>", lambda event: self.send_message())

        # ===== SOCKET =====
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        self.window.mainloop()

    # ===== CHAT BUBBLE =====
    def add_message(self, message):

        bubble = tk.Frame(self.chat_frame, bg="#2ecc71", padx=10, pady=5)

        avatar = tk.Label(
            bubble,
            text=self.nickname[0].upper(),
            bg="#16a085",
            fg="white",
            width=2
        )
        avatar.pack(side=tk.LEFT, padx=5)

        msg = tk.Label(
            bubble,
            text=message,
            bg="#2ecc71",
            wraplength=400,
            justify="left"
        )
        msg.pack(side=tk.LEFT)

        bubble.pack(anchor="w", pady=5, padx=10)

    # ===== SEND MESSAGE =====
    def send_message(self):

        message = self.input_box.get()

        if message != "":
            full_message = f"{self.nickname}: {message}"
            self.client.send(full_message.encode())

        self.input_box.delete(0, tk.END)

    # ===== RECEIVE =====
    def receive(self):

        while True:
            try:
                message = self.client.recv(1024).decode()

                if message == "NICK":
                    self.client.send(self.nickname.encode())

                else:
                    self.window.after(0, self.add_message, message)

            except:
                print("Connection closed")
                self.client.close()
                break

    # ===== EMOJI PICKER =====
    def open_emoji(self):

        emoji_window = tk.Toplevel(self.window)
        emoji_window.title("Emoji")

        emojis = ["😀", "😂", "😍", "👍", "🔥", "❤️"]

        for e in emojis:
            btn = tk.Button(
                emoji_window,
                text=e,
                font=("Arial", 20),
                command=lambda emoji=e: self.insert_emoji(emoji)
            )
            btn.pack(side=tk.LEFT)

    def insert_emoji(self, emoji):
        self.input_box.insert(tk.END, emoji)

    # ===== FILE SHARING =====
    def send_file(self):

        file_path = filedialog.askopenfilename()

        if file_path:
            file_name = file_path.split("/")[-1]
            message = f"{self.nickname} shared file: {file_name}"
            self.client.send(message.encode())

    # ===== DARK MODE =====
    def toggle_mode(self):

        if self.dark_mode:
            self.chat_canvas.config(bg="white")
            self.chat_frame.config(bg="white")
            self.dark_mode = False
        else:
            self.chat_canvas.config(bg="#1e1e1e")
            self.chat_frame.config(bg="#1e1e1e")
            self.dark_mode = True


ChatClient()
