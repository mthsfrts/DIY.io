import os
import socket
from email import message
from select import select

import message_pb2


HOST = 'localhost'
PORT = 5678


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def validate_input(options: str):
    number_of_options = len(options.splitlines()) - 2
    selected_option = input(options)
    while not selected_option.isnumeric() or int(selected_option) < 1 or int(selected_option) > number_of_options:
        clear_console()
        print("Opção Inválida - Digite novamente")
        selected_option = input(options)
    return selected_option


def devices_to_str(device_list):
    msg = "Lista de dispositivos: \n"
    device_list.devices.sort(key=lambda x: x.id)
    for device in device_list.devices:
        msg += f"{device.id} - {device.type}\n"

    msg += "Digite o id do dispositivo desejado: "
    return msg


def initialize_app():
    try:
        s.connect((HOST, PORT))
        print(f'Connected successfully to {HOST}:{PORT}')
    except:
        print(f'Failed to connect {HOST}:{PORT}')
    while True:
        # recebe uma lista de dispositivos do gateway
        device_list_msg = s.recv(10240)
        device_list = message_pb2.DeviceList()
        device_list.ParseFromString(device_list_msg)

        # envia o id do dispositivo escolhido para o gateway
        selected_device = validate_input(devices_to_str(device_list))
        selected_device_msg = message_pb2.Request()
        selected_device_msg.address = HOST
        selected_device_msg.port = PORT
        selected_device_msg.request = selected_device
        s.sendall(selected_device_msg.SerializeToString())

        clear_console()
        # recebe a lista de comandos do dispositivo escolhido
        device_cmds_msg = s.recv(10240)
        device_cmds = message_pb2.Response()
        device_cmds.ParseFromString(device_cmds_msg)

        # seleciona o comando e os argumentos desejados
        selected_cmd = input(device_cmds.response)
        selected_cmd_msg = message_pb2.Request()
        selected_cmd_msg.address = HOST
        selected_cmd_msg.port = PORT
        selected_cmd_msg.request = selected_cmd
        s.sendall(selected_cmd_msg.SerializeToString())

        # recebe o resultado do comando escolhido
        cmd_result_msg = s.recv(10240)
        cmd_result = message_pb2.Response()
        cmd_result.ParseFromString(cmd_result_msg)

        clear_console()
        print(cmd_result.response)
        # break


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
initialize_app()
s.close()
