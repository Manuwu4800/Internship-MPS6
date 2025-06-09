import RPi.GPIO as GPIO
import socket
import os

# GPIO Setup
VALVE_PIN = 12
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
GPIO.setup(VALVE_PIN, GPIO.OUT)
valve_state = None

# Server info
PORT = 5000
ip = os.popen("hostname -I").read().strip()
print(f"[valveServer] Raspberry Pi IP Address: {ip}")
print(f"[valveServer] Listening on port {PORT}…")

# Setup socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("", PORT))
server_socket.listen(5)

try:
    while True:
        print("[valveServer] Waiting for a client…")
        client_socket, client_address = server_socket.accept()
        print(f"[valveServer] Connected with {client_address}")

        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    print("[valveServer] Client disconnected")
                    break

                message = data.decode("utf-8").strip().lower()
                print(f"[valveServer] Command received: {message}")

                try:
                    if message == "open" and valve_state != "open":
                        GPIO.output(VALVE_PIN, GPIO.LOW)
                        valve_state = "open"
                        response = "[valveServer] Valve opened successfully"

                    elif message == "close" and valve_state != "close":
                        GPIO.output(VALVE_PIN, GPIO.HIGH)
                        valve_state = "close"
                        response = "[valveServer] Valve closed successfully"

                    elif message == "exit":
                        response = "[valveServer] Exit command received, but server continue"

                    else:
                        response = "[valveServer] Unknown or redundant command"

                except Exception as gpio_error:
                    response = f"[valveServer] GPIO Error: {gpio_error}"

                print(response)
                client_socket.sendall(response.encode("utf-8"))

        except Exception as e:
            print(f"[valveServer] Error during client session: {e}")

        finally:
            client_socket.close()
            print("[valveServer] Connection closed.")

except KeyboardInterrupt:
    print("[valveServer] Shutting down…")

except Exception as e:
    print(f"[valveServer] Server error: {e}")

finally:
    GPIO.cleanup()
    server_socket.close()
