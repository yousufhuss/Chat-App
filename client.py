import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
from datetime import datetime
import argparse

# Parsing command line arguments
parser = argparse.ArgumentParser(description="Chat Client")
parser.add_argument("host", help="Server IP address")
parser.add_argument("port", type=int, help="Server port")
args = parser.parse_args()


# Choosing nickname
nickname = input("Choose your nickname: ")

# Client setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = args.host
port = args.port

try:
    client.connect((host, port))
except socket.error as e:
    print(f"Connection failed. Error: {str(e)}")
    exit()

# GUI setup

root = tk.Tk()
root.title("Chat Client")


chat_label = tk.Label(root, text="Chat:")
chat_label.pack(padx=20, pady=5)

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', font=('Helvetica', 10))
chat_area.pack(padx=20, pady=5)

message_label = tk.Label(root, text="Message:")
message_label.pack(padx=20, pady=5)

message_entry = tk.Text(root, height=3, width=50, font=('Helvetica', 10))
message_entry.pack(padx=20, pady=5)

def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def send_message():
    message = f'{nickname}: {message_entry.get("1.0", "end-1c")}'
    timestamped_message = f'[{get_timestamp()}] {message}'
    try:
        client.send(timestamped_message.encode('utf-8'))
    except UnicodeEncodeError as e:
        messagebox.showerror("Encoding Error", f"Failed to send message: {e}")
    message_entry.delete("1.0", tk.END)

sendmessageimg = tk.PhotoImage(file='send.png')
send_button = tk.Button(root, image=sendmessageimg, command=send_message ,borderwidth=0)
send_button.pack(padx=20, pady=5)

def insert_emoji(emoji_char):
    message_entry.insert(tk.END, emoji_char)

def open_emoji_dialog():
    emojis = ['😊', '😂', '😍', '😢', '😎', '😡']
    emoji_char = simpledialog.askstring("Select Emoji", "Enter the emoji:", initialvalue=emojis[0])
    if emoji_char in emojis:
        insert_emoji(emoji_char)
    else:
        messagebox.showerror("Invalid Emoji", "Emoji not found in the list.")


emoji_button = tk.Button(root, text="Emoji", command=open_emoji_dialog)
emoji_button.pack(padx=20, pady=5)

def receive():
    while True:
        try:
            # Receive message
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                chat_area.config(state='normal')
                chat_area.insert(tk.END, message + '\n')
                chat_area.yview(tk.END)
                chat_area.config(state='disabled')
        except:
            # Close connection when error
            print('An error occurred!')
            client.close()
            break

# Starting threads for receiving messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

root.mainloop()
