import socket

# Set the server IP address and port
server_ip = "0.0.0.0"  # Replace with the actual IP address of your server
server_port = 8005

while True:
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind((server_ip, server_port))

    # Listen for incoming connections (max 1 connection in the queue)
    server_socket.listen(1)
    print(f"Listening on {server_ip}:{server_port}")

    try:
        # Wait for a connection from the D1 Mini
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        while True:
            command = input(">>")

            if command == "exit":
                # Close the connection
                client_socket.close()
                break

            try:
                client_socket.sendall(command.encode('utf-8'))
            except socket.error as e:
                print(f"Error: {e}")
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the server socket
        server_socket.close()
