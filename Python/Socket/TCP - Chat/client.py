import threading
import socket
from serialize import Serialize

server_ip = '127.0.0.1'
server_port = 5000

# Creating Client
nickname = input("Choose an nickname: ")
print(f"hey, {nickname} to enter in a chatroom please use the command:".upper(), "/enter")
enter = input()

# Getting Server Details
if enter == "/enter":
    host = input("What is the server ip: ")
    port = input("What is the port: ")

    if host != server_ip and int(port) != server_port:
        print("Connection Error, please check the server details!".upper())

    elif host != server_ip and int(port) == server_port:
        print("Ip Error, please check the server ip!".upper())

    elif host == server_ip and int(port) != server_port:
        print("Port Error, please check the server port!".upper())

    else:
        # Establishing Connection
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, int(port)))


def receive():
    """
    Method responsible to receive client messages.
    """

    while True:
        try:
            message = Serialize.unpickle(client.recv(1024))

            # Handling Messages
            if message == "nickname?":
                client.send(Serialize.pickle(nickname))

            else:
                print(message)

        except:
            print('Your chat connection is closed!')
            client.close()
            break


def send():
    """
    Method responsible to encode and send client messages.
    """

    while True:
        message = f'{nickname}: {input("")}'

        # Handling Commands

        # Show all commands
        if message[len(nickname) + 2:].startswith("/help"):
            print("Here all the available commands:\n"
                  "/quit\n"
                  "/list")

        # Getting all the client online
        elif message[len(nickname) + 2:].startswith("/list"):
            client.send(Serialize.pickle(f"LIST"))
            online = Serialize.unpickle(client.recv(1024))

            if len(online) == 1:
                print(online)

            else:
                print(f"clients online :\n".upper(), online)

        # Disconnecting
        elif message[len(nickname) + 2:].startswith("/quit"):
            client.send(Serialize.pickle("QUIT"))
            print('Disconnecting!')
            client.close()
            break

        else:
            client.send(Serialize.pickle(message))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_thread = threading.Thread(target=send)
send_thread.start()
