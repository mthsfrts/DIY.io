# Libraries
import socket as sckt
import sys


class UpdServer:
    # Setting up Server
    prc = 0  # ID of the process.
    host = '127.0.0.1'  # Standard loopback interface address (localhost).
    port = 65432  # Port to listen on (non-privileged ports are > 1023).

    # Setting Socket Connection
    sock = sckt.socket(sckt.AF_INET, sckt.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"Server is up and Running on port : {port}!")
    print("Waiting Client!\n")

    while True:
        try:
            # Treating Encoded Message
            prc += 1  # Enumerating new process
            data, addr = sock.recvfrom(1024)  # Getting Encoded data
            CIp, CPort = addr  # Setting Details
            decoded = data.decode('utf-8')  # Decoding data

            # Client Terminal Return
            print(f"Client's Details:\n"
                  f"Process : {prc}\n"
                  f"IP: {CIp}\n"
                  f"Port: {CPort}\n"
                  f"You gave me the equation: {decoded}\n")

            # Handling Data Variables
            if decoded == "Q" or decoded == "q" or decoded == "Quit" or decoded == "quit" or decoded == "quit()":
                sock.sendto("Quit".encode("utf-8"), addr)
                break

            else:
                result = eval(data)
                sock.sendto(str(result).encode('utf-8'), addr)

        # Handling Error that might appear.
        except ZeroDivisionError:
            sock.sendto("ZeroDiv".encode('utf-8'), addr)
        except ArithmeticError:
            sock.sendto("MathError".encode('utf-8'), addr)
        except SyntaxError:
            sock.sendto("SyntaxError".encode('utf-8'), addr)
        except NameError:
            sock.sendto("NameError".encode('utf-8'), addr)
        except TypeError:
            sock.sendto("TypeError".encode('utf-8'), addr)

        # Stop server by pressing ctrl+C
        except KeyboardInterrupt:
            exit(0)


if __name__ == "__main__":
    UpdServer()
