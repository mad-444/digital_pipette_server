

import pigpio

class DigitalPipette():
    def __init__(self, name, gpio_pin, us_per_uL, zero_position, limit_position, capacity):

        self.gpio_pin = gpio_pin
        self.name = name
        self.us_per_uL = us_per_uL
        self.zero_position = zero_position
        self.limit_position = limit_position
        self.capacity = capacity

        self.pi = pigpio.pi()

        self.current_pulsewidth = 0
        
        self.remaining_volume = None


    def load_syringe(self, volume, pulsewidth):

        self.remaining_volume = volume
        self.current_pulsewidth = pulsewidth






    def dispense(self, volume: float):
        """
        Dispenses desired volume
        """

        assert volume < self.remaining_volume, f'Pipette {self.name} has {self.remaining_volume} uL remaining, but dispense requested {volume} uL'

        new_pulsewidth = self.get_pulsewidth(volume, mode = 'dispense')

        pigpio.set_servo_pulsewidth(self.gpio_pin, new_pulsewidth)

        self.current_pulsewidth = new_pulsewidth
        self.remaining_volume = self.remaining_volume - volume

        return
    
    def aspirate(self, volume: float):
        """
        Aspirates desired volume into syringe for loading
        """

        assert self.remaining_volume + volume < self.capacity, f'Pipette {self.name} has {self.capacity - self.remaining_volume} uL of available capacity by aspirate requested {volume} uL'

        new_pulsewidth = self.get_pulsewidth(volume, mode = 'aspirate')

        pigpio.set_servo_pulsewidth(self.gpio_pin, new_pulsewidth)

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





        


        
