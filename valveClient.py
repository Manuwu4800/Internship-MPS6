import socket
import tkinter as tk
import time

def send_command(command):
    try:
        server_ip = ip_entry.get()
        server_port = int(port_entry.get())
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        client_socket.send(command.encode('utf-8'))
        time.sleep(1.5)
        response = client_socket.recv(1024).decode('utf-8')
        client_socket.close()
        return response

    except Exception as e:
        return f"[Client Error] {e}"

def display_response(message):
    response_label_var.set(message)

def open_valve():
    response = send_command("open")
    display_response(response)

def close_valve():
    response = send_command("close")
    display_response(response)

def exit_program():
    response = send_command("exit")
    display_response(response)
    root.quit()

root = tk.Tk()
root.title("Valve Control")
root.geometry("500x400")  


font_label = ('Arial', 12)
font_button = ('Arial', 12)

# IP
ip_label = tk.Label(root, text="Server IP:", font=font_label)
ip_label.pack(pady=(20, 5))
ip_entry = tk.Entry(root, width=30, font=font_label)
ip_entry.pack()
ip_entry.insert(0, '192.168.1.205')
ip_entry.config(state='readonly')

# Port
port_label = tk.Label(root, text="Server Port:", font=font_label)
port_label.pack(pady=(15, 5))
port_entry = tk.Entry(root, width=30, font=font_label)
port_entry.pack()
port_entry.insert(0, '5000')
port_entry.config(state='readonly')

button_frame = tk.Frame(root)
button_frame.pack(pady=25)

open_button = tk.Button(button_frame, text="Open Valve", command=open_valve, font=font_button, width=15, height=2)
open_button.grid(row=0, column=0, padx=10)

close_button = tk.Button(button_frame, text="Close Valve", command=close_valve, font=font_button, width=15, height=2)
close_button.grid(row=0, column=1, padx=10)

exit_button = tk.Button(root, text="Exit", command=exit_program, font=font_button, width=32, height=2)
exit_button.pack(pady=10)

# Server response
response_label = tk.Label(root, text="Server Response:", font=('Arial', 12, 'bold'))
response_label.pack(pady=(10, 5))

response_label_var = tk.StringVar()
response_label_value = tk.Label(root, textvariable=response_label_var, wraplength=600, justify="center", font=font_label, fg="blue")
response_label_value.pack(pady=5)

root.mainloop()