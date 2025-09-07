import socket
import threading

HOST = '127.0.0.1'  # The loopback address (localhost)
PORT = 1234  # Use any valid port number between 0 and 65535

LISTENER_LIMIT = 5  # The number of clients the server can listen to
active_clients = []  # This list contains all the currently connected users

# Function to listen for all upcoming messages from the client
def listen_for_messages(client, username):

    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + '~' + message
            send_message_to_all(final_msg)
        else:
            print(f"The message sent from client {username} is empty")


# Function to send a message to a single client
def send_message_to_client(client, message):
    client.sendall(message.encode())


# Function to send a message to all clients that are
# currently connected to this server
def send_message_to_all(message):
    # Going through each user connected to the server
    for user in active_clients:
        send_message_to_client(user[1], message)


# Function to handle client:
def client_handler(client):
    # Server will listen for the client message that will contain the username
    while True:
        # 'recv' is the function that stands for receiving
        username = client.recv(2048).decode('utf-8')  # 2048 is the maximum size of the message
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER " + f"{username} added to the chat"
            send_message_to_all(prompt_message)
            break  # Because we have received the client's username
        else:
            print("Client username is empty!")

    # Start the thread to listen for messages after the username is obtained
    threading.Thread(target=listen_for_messages, args=(client, username,)).start()


def main():
    # Creating the socket class object:
    # AF_INET states that we are using IPv4 network addresses
    # SOCK_STREAM states that we are using TCP packets for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Creating a try-except block to bind the server:
    try:
        # Providing the server with an address in the form of a HOST and a PORT
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST}:{PORT}")
    except Exception as e:
        print(f"Unable to bind to host {HOST} and port {PORT}: {e}")
        return

    # Setting the server limit to communicate with limited hosts in a network
    server.listen(LISTENER_LIMIT)
    print(f"Server is listening with a limit of {LISTENER_LIMIT} connections")

    # Now, we'll create a while loop that will keep on listening for client connections
    while True:
        client, address = server.accept()  # 'address' is a tuple (IP, Port)
        print(f"Successfully connected to client {address[0]}:{address[1]}")

        # For the function to run concurrently with the server, we'll use threading
        threading.Thread(target=client_handler, args=(client,)).start()


# Ensuring the script runs the main function
if __name__ == '__main__':
    main()
