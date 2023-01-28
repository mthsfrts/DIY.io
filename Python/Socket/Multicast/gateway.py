import json
import socket
import threading
import time
from collections import deque
from enum import Enum

import message_pb2

ADDRESS = 'localhost'
MCAST_GRP = '225.0.0.250'
MCAST_PORT = 5007
CLIENT_PORT = 5678
DEVICE_PORT = 4321
MULTICAST_TTL = 2
DISCOVER_SLEEP_TIME = 5


class Requests(str, Enum):
    IDENTIFY = "IDENTIFY"
    CMD = "CMD"
    LIST_ACTIONS = "LIST_ACTIONS"


def connect_client():
    while True:
        try:
            client, address = sock_client.accept()

            client_thread = threading.Thread(
                target=handle_client_msgs, args=[client])
            client_thread.start()

        except Exception as err:
            print("Connection failed. (connect_client)")
            print(err)
            # break


def handle_client_msgs(client):

    while True:
        try:
            # Envia lista de client
            time.sleep(0.3)
            devices_list = get_devices_list(devices)
            client.send(devices_list.SerializeToString())
            # client.send(devices_to_str().encode('utf-8'))
            # id = client.recv(10240).decode('utf-8')
            id_request = client.recv(10240)
            id_request_msg = message_pb2.Request()
            id_request_msg.ParseFromString(id_request)
            id = id_request_msg.request

            print(f"{id_request_msg.address} : {id_request_msg.port}")

            # Cliente escolhe device
            if id in devices.keys():
                msg_actions = {"type": Requests.LIST_ACTIONS,
                               "command": "", "target": id}
                send_cmd(msg_actions)
                # Espera pela lista de comandos do device escolhido
                command_list_msg = message_pb2.Response()
                command_list_msg.response = get_message()

                client.send(command_list_msg.SerializeToString())

                selected_cmd = client.recv(10240)
                selected_cmd_msg = message_pb2.Request()
                selected_cmd_msg.ParseFromString(selected_cmd)

                msg_cmd = {"type": Requests.CMD,
                           "command": selected_cmd_msg.request, "target": id}
                send_cmd(msg_cmd)
                # Espera pela confirmacao das alteracoes
                # cmd_info = get_message()

                cmd_info_msg = message_pb2.Response()
                cmd_info_msg.response = get_message()
                client.send(cmd_info_msg.SerializeToString())

            else:
                client.send("Id Invalido".encode('utf-8'))
        except:
            break


def get_message():
    while not message_queue:
        pass
    return message_queue.popleft()


def get_devices_list(devices_dict: dict):
    try:
        # print(devices_dict)
        device_list = message_pb2.DeviceList()

        for id in devices_dict.keys():
            device_msg = message_pb2.Device()
            device_msg.type = devices_dict[id]["type"]
            device_msg.id = id
            device_list.devices.append(device_msg)
        return device_list
    except Exception as e:
        print(e)


def init_multicast():
    msg = {"type": Requests.IDENTIFY, "command": "", "target": "all"}
    serialized_msg = json.dumps(msg)

    while True:
        try:
            sock_multcast.sendto(bytes(serialized_msg, 'utf-8'),
                                 (MCAST_GRP, MCAST_PORT))
            time.sleep(DISCOVER_SLEEP_TIME)
        except Exception as err:
            print("Connection failed. (init_multicast)")
            print(err)


def send_cmd(msg: dict):
    try:
        serialized_msg = json.dumps(msg)
        sock_multcast.sendto(bytes(serialized_msg, 'utf-8'),
                             (MCAST_GRP, MCAST_PORT))
    except Exception as err:
        print("Command failed. (send_cmd)")
        print(err)


def handle_device_msgs(sock_device: socket):
    while True:
        try:
            message = json.loads(
                sock_device.recv(1024).decode('utf-8'))
            if message["req_type"] == Requests.IDENTIFY:
                if message["id"] not in devices:
                    devices[message["id"]] = {"type": message["type"],
                                              "address": message["address"], "port": message["port"]}
                    print(f"Dispositivo adicionado: {message['type']}")

            if message["req_type"] == Requests.CMD:
                message_queue.append(message["content"])

            if message["req_type"] == Requests.LIST_ACTIONS:
                message_queue.append(message["content"])

        except Exception as err:
            print(err)
            break


def connect_devices():
    sock_device = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_device.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock_device.bind((ADDRESS, DEVICE_PORT))
    sock_device.listen(1)

    while True:
        try:
            device, address = sock_device.accept()
            device_thread = threading.Thread(
                target=handle_device_msgs, args=[device])
            device_thread.start()

        except Exception as err:
            print("Connection failed. (connect_devices)")
            print(err)
            # sock_device.close()
            break


def initialize():
    print("Gateway initialized.")

    multicast = threading.Thread(target=init_multicast)
    device_listener = threading.Thread(
        target=connect_devices)
    client_socket = threading.Thread(
        target=connect_client)

    multicast.start()
    device_listener.start()
    client_socket.start()


sock_multcast = socket.socket(
    socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock_multcast.setsockopt(
    socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
sock_multcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

devices = {}
message_queue = deque()

sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock_client.bind((ADDRESS, CLIENT_PORT))
sock_client.listen(1)

initialize()

# sock_multcast.close()
# sock_client.close()
