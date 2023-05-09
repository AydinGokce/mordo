from adafruit_servokit import ServoKit
import json
import time
from utils import get_servo_list
from typing import Tuple


class BodyController:
    def __init__(self, kits: Tuple[ServoKit, ServoKit]):
        
        self.kits = kits
        self.servos = get_servo_list(self.kits)
        assert len(self.kits) == 2, "unexpected number of ServoKit objects"
        
        # totality
        self.max_yaw_magnitude = 45 # (deg), plus and minus        
        
        # yawing
        self.yaw_servo_indices = [4, 6, 8, 10]
        self.yaw_sensitive_pitch_servo_indices = []#[5, 7, 9]
        self.yaw_weights = {
            4: 0.60,
            6: 0.20,
            8: 0.10,
            10: 0.10
        }
    
        # pitching
        self.pitch_servo_indices = [5, 7, 9]
        self.pitch_weights = {
            5: 0.0,
            7: 0.80,
            9: 0.20
        }
        self.pitch_yaw_adjustments = {
            5: 0,
            7: 0,
            9: 0
        }
        
        self._reset_position()

    
    
    def angle_offset_head_yaw(self, yaw_angle: float):
        
        for yaw_servo_index in self.yaw_servo_indices:
            servo_angle = self.yaw_weights[yaw_servo_index] * yaw_angle
            self.servos[yaw_servo_index].apply_angle(servo_angle)
        
        for ysp_servo_index in self.yaw_sensitive_pitch_servo_indices:
            servo_angle = (abs(yaw_angle) / self.max_yaw_magnitude) * (self.servos[ysp_servo_index].flat_point - self.servos[ysp_servo_index].center_angle)
            if ysp_servo_index == 5:
                #TODO this is a band-aid fix for servo 5
                self.pitch_yaw_adjustments[ysp_servo_index] = servo_angle * 0.5
            else:
                self.pitch_yaw_adjustments[ysp_servo_index] = servo_angle
            
            
    def angle_offset_head_pitch(self, pitch_angle: float):
    
        for pitch_servo_index in self.pitch_servo_indices:
            servo_angle = self.pitch_weights[pitch_servo_index] * pitch_angle
            self.servos[pitch_servo_index].apply_angle(servo_angle + self.pitch_yaw_adjustments[pitch_servo_index])
    
    
    def _reset_position(self): 
        for servo in self.servos:
            servo.center()
    
            
