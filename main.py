# main.py -- put your code here!
import machine
#from machine import Pin
import time
#from time import sleep

# Define the pins for LEDs
led_pin_a = machine.Pin(14, machine.Pin.OUT)  # GPIO14 for LED A
led_pin_b = machine.Pin(12, machine.Pin.OUT)  # GPIO12 for LED B

# Create PWM objects
pwm_a = machine.PWM(led_pin_a, freq=1000)  # Frequency = 1000 Hz
pwm_b = machine.PWM(led_pin_b, freq=1000)

# Map the input range (-255 to 255) to PWM range (0-1023)
def map_to_pwm(x_val, x_min, x_max, pwm_min, pwm_max):

    return int(pwm_min + (pwm_max - pwm_min) * (x_val - x_min) / (x_max - x_min))


# a = left wing b = right wing of mosquito

try:
    while True:
        x = int(input("Enter x (-255 to 255): "))
        y = int(input("Enter y (-255 to 255): "))
        
        # Determine the region based on x and y values
        if -5 <= x <= 5 and -5 <= y <= 5:
            pwm_value_a = 0  # Center
            pwm_value_b = 0

        elif -5 <= x <= 5 and 5 < y <= 255:
            pwm_value_a = map_to_pwm(y, 5, 255, 0, 1023)  # Forward
            pwm_value_b = map_to_pwm(y, 5, 255, 0, 1023)

        elif -5 <= x <= 5 and -255 <= y < -5:
            pwm_value_a = map_to_pwm(y, -255, -5, 0, 1023)  # Backward
            pwm_value_b = map_to_pwm(y, -255, -5, 0, 1023)

        elif 5 < x <= 255 and -5 <= y <= 5:
            pwm_value_a = map_to_pwm(x, 5, 255, 0, 1023)  # Right
            pwm_value_b = map_to_pwm(x, 5, 255, 0, 1023)

        elif -255 <= x < -5 and -5 <= y <= 5:
            pwm_value_a = map_to_pwm(x, -255, -5, 1023, 0)  # Left
            pwm_value_b = map_to_pwm(x, -255, -5, 1023, 0)


        elif 5 < x <= 255 and 5 < y <= 255: # Top right
              
            # x>y 
            if x > y:
                a_map = map_to_pwm(y, 5, 255, 0, 1023)
                pwm_value_a = map_to_pwm(x, y, 255, a_map, 1023)
                b_map = map_to_pwm(y, 5, 255, 1023, 0)  
                pwm_value_b = map_to_pwm(x, y, 255, 0, b_map)   
            # y>x
            else:
                pwm_value_a = map_to_pwm(y, 5, 255, 0, 1023)
                b_map = map_to_pwm(y, 5, 255, 0, 1023)  
                pwm_value_b = map_to_pwm(x, 5, y, b_map, 0)    


        elif -255 <= x < -5 and 5 < y <= 255:  # Top left


            # x>y 
            if abs(x) > y:
                a_map = map_to_pwm(y, 5, 255, 1023, 0)
                pwm_value_a = map_to_pwm(x, -255, -y, a_map, 0)
                b_map = map_to_pwm(y, 5, 255, 0, 1023)  
                pwm_value_b = map_to_pwm(x, -255, -y, 1023, b_map)   
            # y>x
            else:
                b_map = map_to_pwm(y, 5, 255, 0, 1023)  
                pwm_value_a = map_to_pwm(x, -y, -5, 0, b_map)   #change -255 to st line
                pwm_value_b = map_to_pwm(y, 5, 255, 0, 1023) 


        elif 5 < x <= 255 and -255 <= y < -5:   # Bottom right

            # x>y 
            if abs(x) > abs(y):
                a_map = map_to_pwm(y, -5, -255, 0, 1023)
                pwm_value_a = map_to_pwm(x, -255, y, 1023, a_map)
                b_map = map_to_pwm(y, -5, -255, 1023, 0)  
                pwm_value_b = map_to_pwm(x, -255, y, b_map, 0)   
            # y>x
            else:
                pwm_value_a = map_to_pwm(y, -5, -255, 0, 1023)
                b_map = map_to_pwm(y, -5, -255, 0, 1023)  
                pwm_value_b = map_to_pwm(x, y, -5, 0, b_map) 


        elif -255 <= x < -5 and -255 <= y < -5:  # Bottom left


            # x>y 
            if x > abs(y):
                a_map = map_to_pwm(y, -5, -255, 1023, 0)
                pwm_value_a = map_to_pwm(x, -y, 255, 0, a_map)
                b_map = map_to_pwm(y, -5, -255, 0, 1023)  
                pwm_value_b = map_to_pwm(x, -y, 255, b_map, 1023)   
            # y>x
            else:
                a_map = map_to_pwm(y, -5, -255, 0, 1023)
                pwm_value_a = map_to_pwm(x, -5, -y, a_map, 0)
                pwm_value_b = map_to_pwm(y, -5, -255, 0, 1023) 
        
        print("pwm_a", pwm_value_a, " ", "pwm_b", pwm_value_b)

        # Apply PWM to LEDs
        pwm_a.duty(pwm_value_a)
        pwm_b.duty(pwm_value_b)
        
        time.sleep(1)  # Update the PWM values every 1 second
        
finally:
    # Turn off PWM and cleanup
    pwm_a.deinit()
    pwm_b.deinit()

