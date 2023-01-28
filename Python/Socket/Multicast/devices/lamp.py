import time
from enum import Enum, IntEnum

from devices.device import Device


class Color(str, Enum):
    WHITE = "BRANCO"
    RED = "VERMELHO"
    GREEN = "VERDE"
    BLUE = "AZUL"
    YELLOW = "AMARELO"
    ORANGE = "LARANJA"


class Actions(IntEnum):
    CHANGE_COLOR = 1
    CHANGE_INTENSITY = 2
    SWITCH_POWER = 3
    GET_INFO = 4


class Intensity(str, Enum):
    LOW = "BAIXO"
    MEDIUM = "MEDIO"
    HIGH = "ALTO"


class Lamp(Device):
    def __init__(self, type, id) -> None:
        super().__init__(type, id)
        self.color: Color = Color.WHITE
        self.power: bool = True
        self.intensity: Intensity = Intensity.MEDIUM
        self.actions_map: dict = {Actions.CHANGE_COLOR: self.change_color, Actions.CHANGE_INTENSITY: self.change_intensity,
                                  Actions.SWITCH_POWER: self.switch_power, Actions.GET_INFO: self.get_info}

    def actions_to_string(self, enum: Actions):
        match enum:
            case Actions.CHANGE_COLOR:
                return "Trocar cor (Branco, Vermelho, Verde, Azul...)"
            case Actions.CHANGE_INTENSITY:
                return "Mudar intensidade (Baixo, medio ou alto)"
            case Actions.SWITCH_POWER:
                return "Ligar/Desligar"
            case Actions.GET_INFO:
                return "Ver informações"

    def change_color(self, color: Color):
        if self.power == False:
            return "Dispositivo Desligado"
        if not self.is_valid_arg(color, Color):
            return "Cor invalida"
        self.color = color
        return f"Cor atualizada: {self.color}"

    def change_intensity(self, intensity: Intensity):
        if self.power == False:
            return "Dispositivo Desligado"
        if not self.is_valid_arg(intensity, Intensity):
            return "Intensidade Invalida"
        self.intensity = intensity
        return f"Intensidade atualizada: {self.intensity}"

    def switch_power(self):
        self.power = not self.power
        return f"Status de Energia: {'Ligada' if self.power else 'Desligada'}"

    def get_info(self):
        if self.power == False:
            return "Dispositivo desligado\n"
        info = f"""
===============================
Informações do dispositivo\n
- Cor da luz: {self.color}\n
- Intensidade da luz: {self.intensity}\n
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
