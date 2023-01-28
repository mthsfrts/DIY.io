# Libraries
import socket as sckt


class UdpClient:
    try:
        # Setting up Client
        host = "localhost"
        port = 65432

        # Setting Socket Connection
        sock = sckt.socket(sckt.AF_INET, sckt.SOCK_DGRAM)

        # Setting Timer
        timer = 0.1

        while True:
            equation = input("Please give me your equation (Ex: 2+2) or Q to quit: ")
            sock.sendto(bytes(equation, "utf-8"), (host, port))
            result = sock.recv(1024).decode("utf-8")

            if result == "Q" or result == "q" or result == "Quit" or result == "quit" or result == "quit()":
                print("Closing client connection, goodbye")
                break

            elif result == "ZeroDiv":
                print("You can't divide by 0, try again")

            elif result == "MathError":
                print("There is an error with your math, try again")

            elif result == "SyntaxError":
                print("There is a syntax error, please try again")

            elif result == "NameError":
                print("You did not enter an equation, try again")

            else:
                print("The answer is:", result)

        sock.close()  # Close the socket when done

    except (IndexError, ValueError):
        print("You did not specify an IP address and port number")


if __name__ == "__main__":
    UdpClient()
