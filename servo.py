from typing import Literal, Union, Tuple
import json
import warnings
from adafruit_servokit import ServoKit

class Servo:
    def __init__(self, kits: Tuple[ServoKit, ServoKit], index: int, axis: Literal["pitch", "yaw", "yaw_sensitive_pitch"], min_angle: float, center_angle: float, max_angle: float, flat_point: float = None):
        self.kits = kits
        self.index = index
        self.axis = axis
        self.min_angle = min_angle
        self.center_angle = center_angle
        self.max_angle = max_angle
        self.flat_point = flat_point


    @staticmethod
    def from_json(json_servo: Union[str, dict], kits: Tuple[ServoKit, ServoKit]) -> 'Servo':
        if isinstance(json_servo, str):
            json_servo = json.loads(json_servo)
        
        if "flat_point" not in json_servo.keys():
            return Servo(
                kits,
                json_servo["index"],
                json_servo["axis"],
                float(json_servo["min_angle"]),
                float(json_servo["center_angle"]),
                float(json_servo["max_angle"])
            )
            
        else:
            return Servo(
                kits,
                json_servo["index"],
                json_servo["axis"],
                float(json_servo["min_angle"]),
                float(json_servo["center_angle"]),
                float(json_servo["max_angle"]),
                flat_point=float(json_servo["flat_point"])
            )


    def apply_angle(self, angle: float):
        
        if angle + self.center_angle > self.max_angle:
            warnings.warn(f"[Servo {self.index}]: attempting to write write over max angle ({angle + self.center_angle} > {self.max_angle}). Truncating.")
            #angle = self.max_angle
            return
        elif angle + self.center_angle < self.min_angle:
            warnings.warn(f"[Servo {self.index}]: attempting to write write under min angle ({angle + self.center_angle} < {self.min_angle}). Truncating.")
            #angle = self.min_angle
            return
        
        if self.index < 16:
            self.kits[0].servo[self.index].angle = angle + self.center_angle
        else:
            self.kits[1].servo[self.index - 16].angle = angle + self.center_angle


    def add_angle(self, angle: float):
        
        if self.index < 16:
            curr_angle = self.kits[0].servo[self.index].angle
        else:
            curr_angle = self.kits[1].servo[self.index - 16].angle
        
        self.apply_angle(curr_angle + angle)
        
        
    def center(self):
        self.apply_angle(0)
