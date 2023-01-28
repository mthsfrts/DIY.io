from enum import Enum
from device import Device


class Actions(str, Enum):
    CHANGE_CHANNEL = 1
    CHANGE_VOLUME = 2
    SWITCH_POWER = 3
    GET_INFO = 4


class StatusPower(str, Enum):
    OFF = "OFF"
    ON = "ON"


class Television(Device):
    def __init__(self, type) -> None:
        super().__init__(type)
        self.channel: int = 10
        self.power: bool = True
        self.volume: int = 10
        # self.actions_map

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

    def change_channel(self, channel: int):
        self.channel = channel

    def change_volume(self, volume: int):
        self.volume = volume

    def switch_power(self, power: StatusPower):
        if power == StatusPower.ON:
            self.power = True
        if power == StatusPower.OFF:
            self.power = False

    def get_info(self):
        info = "Info."
        return info

    def list_actions(self):
        msg = f"{self.type} - Lista de comandos\n"
        for id in Actions:
            msg += f"{id.value} - {self.actions_to_string(id)}\n"
        msg += "Dispositivo Desejado - Comando: "
        return msg

    def select_action(self, command: str):
        pass