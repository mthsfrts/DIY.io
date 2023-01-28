#!/usr/bin/env python3

# Libraries
from scapy.all import *
import sys


def port_scanner():
    """Main Method that will creat the packet and sent to the network, iterating on the range of ports that you will
    set. This was possible by editing the original script from David Bombal"""

    # Checking Command Line
    if len(sys.argv) != 5:
        print("Usage: %s ,source port, target ip, start port, end port" % (sys.argv[0]))
        print(" e.g : sudo python3 port_scanner.py 80 192.168.0.1 22 80")
        sys.exit(0)

    srcport = int(sys.argv[1])
    target = str(sys.argv[2])
    startport = int(sys.argv[3])
    endport = int(sys.argv[4])

    # 3-way handshake
    print("Scanning " + target + " for open TCP ports\n")
    for ports in range(startport, endport + 1):
        try:
            pkt = IP(dst=target) / TCP(sport=srcport, dport=ports, flags='S')
            response = sr1(pkt, timeout=0.2, verbose=0)

            if response.haslayer(TCP) and response.getlayer(TCP).flags == 0x12:
                sr(IP(dst=target) / TCP(dport=response.sport, flags='R'), timeout=0.2, verbose=0)
                print("Target Port " + str(ports) + " is open!")

        except (AttributeError, IndexError, ValueError):
            print(f"The Port: {ports} of the target: {target}, could not be reached!!")

    print("Scan is complete!")


if __name__ == "__main__":
    port_scanner()
