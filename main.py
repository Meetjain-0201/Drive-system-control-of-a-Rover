import network
import socket
import ujson as json
from machine import Pin
from machine import PWM

# WiFi settings
SSID = "AndroidAP"
PASSWORD = "pwdpwdpwd"

# Static IP configuration
STATIC_IP = "192.168.43.45"
SUBNET_MASK = "255.255.255.0"
GATEWAY_IP = "192.168.43.1"

# Create WiFi connection
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

# Configure static IP
wifi.ifconfig((STATIC_IP, SUBNET_MASK, GATEWAY_IP, GATEWAY_IP))

# Wait for WiFi connection
while not wifi.isconnected():
    pass

# Server settings
ESP8266_IP = STATIC_IP  # Use the static IP you've set
ESP8266_PORT = 5050    # Use port 8080 to match Flask app's configuration

# Define the pins for LEDs
led_pin_a = Pin(14, Pin.OUT)  # GPIO14 for LED A
led_pin_b = Pin(12, Pin.OUT)  # GPIO12 for LED B

# Create PWM objects
pwm_a = PWM(led_pin_a, freq=1000)  # Frequency = 1000 Hz
pwm_b = PWM(led_pin_b, freq=1000)

# Map the input range (-255 to 255) to PWM range (0-1023)
def map_to_pwm(x_val, x_min, x_max, pwm_min, pwm_max):
    return int(pwm_min + (pwm_max - pwm_min) * (x_val - x_min) / (x_max - x_min))

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the specified IP address and port
server_socket.bind((ESP8266_IP, ESP8266_PORT))

# Listen for incoming connections
server_socket.listen(1)

print("ESP8266 server listening...")

while True:
    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()
    print("Client connected:", client_address)

    # Receive data from the client
    data = client_socket.recv(1024).decode()
    print("Received data:", data)

    # Parse the received data (assuming it's in JSON format)
    try:
        data_dict = json.loads(data)
        x = data_dict.get("x")
        y = data_dict.get("y")

        if x is not None and y is not None:
            print(f"Received joystick data: x={x}, y={y}")
            
            # Your coordinate processing logic here...
            # (Use the same logic you provided in the previous code snippet)
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
            
            print("pwm_a", pwm_value_a, " ", "pwm_b", pwm_value_b)
            
        else:
            print("Invalid data format")
    except Exception as e:
        print("Error parsing data:", e)

    # Close the client socket
    client_socket.close()
