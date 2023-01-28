import time

from devices.device import DeviceType
from devices.lamp import Lamp
from devices.television import Television
from devices.temp_sensor import TempSensor

lamp = Lamp(DeviceType.LAMP, "1")
sensor = TempSensor(DeviceType.TEMP_SENSOR, "2")
television = Television(DeviceType.TELEVISION, "3")
lamp1 = Lamp(DeviceType.LAMP, "4")
sensor1 = TempSensor(DeviceType.TEMP_SENSOR, "5")
time.sleep(10)
television1 = Television(DeviceType.TELEVISION, "6")
television2 = Television(DeviceType.TELEVISION, "7")
