import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import time

class UDPChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UDP Chat App")

        self.message_box = scrolledtext.ScrolledText(root, width=40, height=10)
        self.message_box.pack(padx=10, pady=10)

        self.entry_message = tk.Entry(root, width=30)
        self.entry_message.pack(pady=5)

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        self.start_button = tk.Button(root, text="Start Receiving", command=self.start_receiving)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop Receiving", command=self.stop_receiving, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.exit_button = tk.Button(root, text="Exit", command=self.exit_app)
        self.exit_button.pack(pady=5)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_thread = None
        self.receive_running = False

    def receive_messages(self):
        while self.receive_running:
            try:
                data, addr = self.sock.recvfrom(1024)
                message = f"Received from {addr}: {data.decode()}\n"
                self.message_box.insert(tk.END, message)
                self.message_box.see(tk.END)
                pass
            except socket.error as e:

                print(f"Error receiving data: {e}")
                break

    def start_receiving(self):
        self.receive_running = True
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()
        self.start_button["state"] = tk.DISABLED
        self.stop_button["state"] = tk.NORMAL

    def stop_receiving(self):
        self.receive_running = False
        self.receive_thread.join()
        self.start_button["state"] = tk.NORMAL
        self.stop_button["state"] = tk.DISABLED

    def send_message(self):
        message = self.entry_message.get()
        self.sock.sendto(message.encode(), (remote_ip, remote_port))
        self.entry_message.delete(0, tk.END)

    def exit_app(self):
        self.sock.close()
        self.root.destroy()


remote_ip = '192.168.116.157'
remote_port = 8080
local_ip = '192.168.116.196'
local_port = 12002
root = tk.Tk()
app = UDPChatApp(root)


app.sock.bind((local_ip, local_port))


root.mainloop()
