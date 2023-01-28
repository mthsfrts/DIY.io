import threading
import socket
from serialize import Serialize

# Creating Server
host = "127.0.0.1"
port = 5000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(5)

# Creating List
clients = []
nicknames = []


def broadcast(message, client):
    """
    Method responsible to broadcast client message through the chatroom
    """
    for c in clients:
        if c != client:
            c.send(Serialize.pickle(f"{message}"))


def handle_client(client):
    """
    Method responsible to handle client connections
    """
    while True:
        try:
            # getting client message
            check = message = Serialize.unpickle(client.recv(1024))

            # checking client message for commands
            if check.startswith("QUIT"):
                index = clients.index(client)  # getting the index of the particular client
                clients.remove(client)  # removing in case of an error
                nickname = nicknames[index]  # bind the nickname to the client by index
                broadcast(f'{nickname} has left the chat!'.upper(), client)  # broadcasting the close connection
                print(f'{nickname} has left the server!')  # Terminal return close client connection
                nicknames.remove(nickname)  # removing nickname
                client.close()  # closing client connection
                continue

            elif check.startswith("LIST"):

                if len(nicknames) == 1:
                    client.send(Serialize.pickle("Your are the only client in the chat!".upper()))

                else:
                    client.send(Serialize.pickle(f"{nicknames}"))
                continue

            else:
                broadcast(message, client)  # broadcasting messages


        except:
            break


def main_receive():
    """
    Method responsible to receive the client connections
    """
    while True:
        try:
            # Server Status
            print("Server is running and listening ...")

            # starting the accept method and splitting the details into client and addresses
            client, address = sock.accept()

            # Server Terminal Return
            print(f"Connection is established with {str(address)}!")

            # Getting nickname
            client.send(Serialize.pickle("nickname?"))
            nickname = Serialize.unpickle(client.recv(1024))

            # Server Terminal Details Return
            print(f"The client's nickname is: {nickname}")

            # Greeting the Client
            client.send(Serialize.pickle("You are connected!\n".upper()))
            client.send(Serialize.pickle(f"Welcome to the chat, {nickname}!".upper()))

            # Populating lists
            nicknames.append(nickname)
            clients.append(client)

            # Broadcast New Connection
            broadcast(f'{nickname} has connected.'.upper(), client)

            # Starting Threads
            thread = threading.Thread(target=handle_client, args=(client,))
            thread.start()

        except KeyboardInterrupt:
            print(f"\nINFO: KeyboardInterrupt".upper())
            print("Closing all sockets and exiting chat server...".upper())
            sock.close()
            exit(0)


if __name__ == "__main__":
    main_receive()
