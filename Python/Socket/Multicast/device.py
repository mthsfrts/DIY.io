import json
import socket
import struct
import threading
from abc import ABC, abstractmethod
from enum import Enum
from uuid import uuid4

ADDRESS_MULTICAST = ('225.0.0.250', 5007)
ADDRESS_TCP = ('localhost', 4321)


class Requests(str, Enum):
    IDENTIFY = "IDENTIFY"
    CMD = "CMD"
    LIST_ACTIONS = "LIST_ACTIONS"


class DeviceType(str, Enum):
    LAMP = "lamp"
    TELEVISION = "television"
    TEMP_SENSOR = "temp_sensor"
    SMOKE_SENSOR = "smoke_sensor"
    UNIDENTIFIED = "unidentified"


class Device(ABC):
    def __init__(self, type) -> None:
        self.id = str(uuid4())
        self.type: DeviceType = type
        self.listen = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        identification_sender = threading.Thread(
            target=self.connect)
        identification_sender.start()

    @abstractmethod
    def get_info(self):
        pass

    @abstractmethod
    def list_actions(self):
        pass

    @abstractmethod
    def select_action(self, command: str):
        pass

    @abstractmethod
    def actions_to_string(self, Actions: Enum):
        pass

    def get_action_by_id(self, id: str, Actions: Enum):
        for action in Actions:
            if action.value == int(id):
                return action
        print("Não achou o action")
        return "0"

    def is_valid_arg(self, arg: str, enum: Enum):
        values = [x.value for x in enum]
        if arg in values:
            return True
        return False

    def connect(self):
        # Listen
        self.listen.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen.bind(ADDRESS_MULTICAST)
        mreq = struct.pack('4sl', socket.inet_aton(
            ADDRESS_MULTICAST[0]), socket.INADDR_ANY)
        self.listen.setsockopt(
            socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # Sender
        info_msg = {"id": self.id, "req_type": Requests.IDENTIFY, "type": self.type,
                    "address": ADDRESS_TCP[0], "port": ADDRESS_TCP[1]}
        serialized_info = json.dumps(info_msg)

        self.sender.connect(ADDRESS_TCP)

        while True:
            try:
                request = json.loads(self.listen.recv(10240).decode('utf-8'))

                if request["type"] == Requests.IDENTIFY:
                    self.sender.sendall(serialized_info.encode("utf-8"))
                if request["type"] == Requests.CMD:
                    if request["target"] == self.id:
                        info = self.select_action(request["command"])
                        msg = {
                            "id": self.id, "req_type": Requests.CMD, "content": info}
                        serialized_msg = json.dumps(msg)
                        self.sender.sendall(serialized_msg.encode("utf-8"))

                if request["type"] == Requests.LIST_ACTIONS:
                    if request["target"] == self.id:
                        actions_list = self.list_actions()
                        msg = {
                            "id": self.id, "req_type": Requests.LIST_ACTIONS, "content": actions_list}
                        serialized_msg = json.dumps(msg)
                        self.sender.sendall(serialized_msg.encode("utf-8"))
            except Exception as err:
                # print("Fui incapaz de mandar mensagem")
                print(err)
                break
