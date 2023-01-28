from enum import IntEnum

from devices.device import Device


class Actions(IntEnum):
    CHANGE_CHANNEL = 1
    CHANGE_VOLUME = 2
    SWITCH_POWER = 3
    GET_INFO = 4


class Television(Device):
    def __init__(self, type, id) -> None:
        super().__init__(type, id)
        self.channel: int = 10
        self.power: bool = True
        self.volume: int = 10
        self.actions_map: dict = {Actions.CHANGE_VOLUME: self.change_volume, Actions.CHANGE_CHANNEL: self.change_channel,
                                  Actions.SWITCH_POWER: self.switch_power, Actions.GET_INFO: self.get_info}

    def actions_to_string(self, enum: Actions):
        match enum:
            case Actions.CHANGE_CHANNEL:
                return "Mudar de canal"
            case Actions.CHANGE_VOLUME:
                return "Ajustar volume"
            case Actions.SWITCH_POWER:
                return "Ligar/Desligar - (ON/OFF)"
            case Actions.GET_INFO:
                return "Ver informações"

    def change_channel(self, channel: str):
        if self.power == False:
            return "Dispositivo Desligado"
        if not channel.isnumeric():
            return "Canal Inválido"
        self.channel = channel
        return f"Canal atualizado: {self.channel}"

    def change_volume(self, volume: str):
        if self.power == False:
            return "Dispositivo Desligado"
        if not volume.isnumeric():
            return "Volume Inválido"
        if int(volume) < 0 or int(volume) > 100:
            return "Volume Inválido: escolha um valor entre 0 e 100."
        self.volume = volume
        return f"Volume atualizado: {self.volume}"

    def switch_power(self):
        self.power = not self.power
        return f"Status da Televisão: {'Ligada' if self.power else 'Desligada'}"

    def get_info(self):
        if self.power == False:
            return "Dispositivo desligado\n"
        info = f"""
===============================
Informações do dispositivo\n
- Canal atual: {self.channel}\n
- Volume: {self.volume}\n
===============================
"""
        return info

    def list_actions(self):
        msg = f"{self.type} - Lista de comandos\n"
        for id in Actions:
            msg += f"{id.value} - {self.actions_to_string(id)}\n"
        msg += "Dispositivo Desejado - Comando: "
        return msg

    def select_action(self, command: str):
        # CMD field1:arg1,field2,arg2,field3,arg3

        cmd_args = command.split()
        cmd = cmd_args[0]

        args = ""
        if len(cmd_args) > 1:
            args = cmd_args[1]

        action = self.get_action_by_id(cmd, Actions)

        if not action:
            return "Ação Inválida"

        # No args
        if action == Actions.SWITCH_POWER:
            return self.switch_power()
        if action == Actions.GET_INFO:
            return self.get_info()

        return self.actions_map[action](args.upper())
