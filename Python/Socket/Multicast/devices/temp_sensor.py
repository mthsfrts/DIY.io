import random
import threading
import time
from enum import Enum, IntEnum
from devices.device import Device

# Este dispositivo vai atuar como tools contínuo, que envia a cada ciclo de X segundos um valor para o Gateway
# esse device vamos ter que tratar de maneira diferente


class Actions(IntEnum):
    CHANGE_SCALE = 1
    GET_INFO = 2


class Scale(str, Enum):
    CELSIUS = "C"
    FAHRENHEIT = "F"


class TempSensor(Device):
    def __init__(self, type, id) -> None:
        super().__init__(type, id)
        self.scale: str = Scale.CELSIUS
        self.temperature: float = 20.0
        self.actions_map: dict = {Actions.CHANGE_SCALE: self.change_scale,
                                  Actions.GET_INFO: self.get_info}
        self.temperature_checker = threading.Thread(
            target=self.calculate_temperature)
        self.temperature_checker.start()

    def actions_to_string(self, enum: Actions):
        match enum:
            case Actions.CHANGE_SCALE:
                return "Mudar escala - (C | F)"
            case Actions.GET_INFO:
                return "Ver Temperatura"

    def calculate_temperature(self):
        while True:
            value = random.uniform(20.5, 23.5)
            if self.scale == Scale.FAHRENHEIT:
                value = (value * (9/5)) + 32
            self.temperature = round(value, 1)
            time.sleep(3)

    def change_scale(self, scale: Scale):
        if not self.is_valid_arg(scale, Scale):
            return "Escala invalida"
        self.scale = scale
        return f"Escala atualizada para {'Fahrenheit' if self.scale == Scale.FAHRENHEIT else 'Celsius'}"

    def get_info(self):
        return f"{self.temperature} - {self.scale}°"

    def list_actions(self):
        msg = f"{self.type} - Lista de comandos\n"
        for id in Actions:
            msg += f"{id.value} - {self.actions_to_string(id)}\n"
        msg += "Dispositivo Desejado - Comando: "
        return msg

    def select_action(self, command: str):
        cmd_args = command.split()
        cmd = cmd_args[0]

        args = ""
        if len(cmd_args) > 1:
            args = cmd_args[1]

        action = self.get_action_by_id(cmd, Actions)

        if not action:
            return "Ação Inválida"

        # No args
        if action == Actions.GET_INFO:
            return self.get_info()

        return self.actions_map[action](args.upper())
#
