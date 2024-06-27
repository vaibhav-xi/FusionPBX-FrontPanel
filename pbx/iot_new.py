import socket
import threading

# Set the server IP address and port
server_ip = "0.0.0.0"  # Replace with the actual IP address of your server
server_port = 8005

# Create a list to store connected clients
clients = []

def handle_client(client_socket):
    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8')
            
            # If the client disconnects, remove it from the list
            if not data:
                clients.remove(client_socket)
                print(f"Client {client_socket.getpeername()} disconnected.")
                break

            print(f"Received command from client: {data}")

            # Broadcast the command to all other connected clients
            for other_client in clients:
                if other_client != client_socket:
                    try:
                        other_client.sendall(data.encode('utf-8'))
                    except socket.error as e:
                        print(f"Error sending data to client: {e}")
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        # Close the client socket
        client_socket.close()

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((server_ip, server_port))

# Listen for incoming connections
server_socket.listen(5)
print(f"Listening on {server_ip}:{server_port}")

while True:
    # Wait for a connection from a client
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    # Add the client socket to the list
    clients.append(client_socket)

    # Create a thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
