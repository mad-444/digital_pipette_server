import pigpio
import json
import numpy as np
import time
import warnings

import logging

logger = logging.getLogger(__name__)

class DigitalPipette():
    def __init__(self, name, gpio_pin, us_per_uL, full_position, empty_position, capacity, time_step_size, min_pw_step):

        self.gpio_pin = gpio_pin
        self.name = name
        self.us_per_uL = us_per_uL
        self.full_position = full_position
        self.empty_position = empty_position
        self.capacity = capacity
        self.time_step_size = time_step_size
        self.min_pw_step = min_pw_step
        self.pi = pigpio.pi()

        self.current_pulsewidth = 0
        
        self.remaining_volume = None

        self.syringe_loaded = False

        logging.debug(f'Initialized syringe {name} on gpio pin {gpio_pin}')
   

    @classmethod
    def from_config(cls, fp):
        with open(fp) as f:
            kwargs = json.load(f)

        return cls(**kwargs)


    def load_syringe(self, volume, pulsewidth):

        self.remaining_volume = volume
        self.current_pulsewidth = pulsewidth

        self.syringe_loaded = True

        return

    def dispense(self, volume: float, s: int = 100):
        """
        Dispenses desired volume

        :param volume: volume of liquid to dispense in uL
        :type volume: float
        :param s: speed to dispense at. speed compliance is best effort within constraints of physical system
        :type s: int
        """

        assert self.syringe_loaded, 'Syringe not loaded'

        assert volume < self.remaining_volume, f'Pipette {self.name} has {self.remaining_volume} uL remaining, but dispense requested {volume} uL'

        new_pulsewidth = self.get_pulsewidth(volume, mode = 'dispense')

        self.set_pulsewidth_speed(new_pulsewidth, s = s)

        self.current_pulsewidth = new_pulsewidth
        self.remaining_volume = self.remaining_volume - volume

        return
    
    def aspirate(self, volume: float, s: int = 100):
        """
        Aspirates desired volume into syringe for loading

        :param volume: Volume of liquid to aspirate in uL
        :type volume: float
        :param s: Speed of aspiration in uL/s. Speed compliance is best effort within the physical constraints of the system
        :type s: int
        """
        assert self.syringe_loaded, 'Syringe must be loaded '
        assert self.remaining_volume + volume < self.capacity, f'Pipette {self.name} has {self.capacity - self.remaining_volume} uL of available capacity by aspirate requested {volume} uL'

        new_pulsewidth = self.get_pulsewidth(volume, mode = 'aspirate')


        self.set_pulsewidth_speed(volume, s = s)

        self.current_pulsewidth = new_pulsewidth
        self.remaining_volume = self.remaining_volume + volume

    def get_pulsewidth(self, volume, mode):
        """
        Convert a volume into a pulsewidth value
        """

        delta_pulsewidth = volume * self.us_per_uL

        if mode == 'dispense':
            new_pulsewidth = self.current_pulsewidth + delta_pulsewidth

        if mode == 'aspirate':
            new_pulsewidth = self.current_pulsewidth - delta_pulsewidth

        return new_pulsewidth
    
    def set_pulsewidth(self, pulsewidth):
        self.pi.set_servo_pulsewidth(self.gpio_pin, pulsewidth)
        self.current_pulsewidth = pulsewidth
        return

    def set_pulsewidth_speed(self, pulsewidth, s = 100):
        """
        Set servo signal pulsewidth to a new value with speed control
        Speed control is implemented in software by moving the servo in small sub-steps on a timer to approximate a slower move. 
        """
        step_size, sign, n_steps = self._calculate_stepped_move(pulsewidth, s)

        for i in range(n_steps):
            move_to_pw = self.current_pulsewidth+(step_size*sign)
            #print('moving to pulsewidth ', move_to_pw)
            self.set_pulsewidth(move_to_pw)
            self.current_pulsewidth = move_to_pw
            time.sleep(self.time_step_size)
        
        # set final pulsewidth to make sure we get there 
        self.set_pulsewidth(pulsewidth)
        self.current_pulsewidth = pulsewidth

    def _calculate_stepped_move(self, pulsewidth, s):
        """
        Calculate step size and n_steps parameters for a stepped speed-controlled move
        """
        #print(f'calculating steps for pulsewidth {pulsewidth} and speed {s}')
        delta_pulsewidth = pulsewidth - self.current_pulsewidth
        #print('delta: ', delta_pulsewidth)
        logging.debug(f'pulsewidth total change: {delta_pulsewidth}')

        # account for direction of move 
        if delta_pulsewidth < 0:
            sign = -1
        else:
            sign = 1
        
        # calculate step size (servo signal step change) from speed in uL/s, conversion factor, and time step
        step_size = s * self.us_per_uL * self.time_step_size
        
        #print('calculated step size is ', step_size, ' uS')
        if step_size < self.min_pw_step:
            warnings.warn(f'Required step size is below minimum step size. Actual speed will be {self.min_pw_step/(self.us_per_uL*self.time_step_size)}')
            step_size = self.min_pw_step

        #print('corrected/actual step size is ', step_size)

        logging.debug(f'PW step size: [uS]: {step_size}')

        n_steps = abs(int(np.floor(delta_pulsewidth/step_size))) - 1
        logging.debug(f'n_steps: {n_steps}')
        #print('number of steps is ', n_steps)

        return step_size, sign, n_steps







        


        
