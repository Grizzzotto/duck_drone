import socket
import time
from rpi_hardware_pwm import HardwarePWM


#Server settings
SERVER_HOST = "192.168.0.109"
SERVER_PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))

print(f"UDP server is running on {SERVER_HOST}:{SERVER_PORT}")


# PWM settings
pwm0 = HardwarePWM(pwm_channel=0, hz=50, chip=0)
pwm0.start(100) # full duty cycle

pwm1 = HardwarePWM(pwm_channel=0, hz=50, chip=0)
pwm1.start(100) # full duty cycle

pwm0.change_duty_cycle(7.5)
pwm1.change_duty_cycle(7.5)

try:
    while True:
        data, client_address = server_socket.recvfrom(1024)
        numbers = list(map(int, data.decode().split(',')))
        print(f"Accepted: {numbers}")
        int_pwm0 = numbers[0]
        if int_pwm0 >= 100 and numbers <= 200:
            pwm0.change_duty_cycle(int_pwm0 / 20)
            time.sleep(3)
except KeyboardInterrupt:
    print("Exiting gracefully...")
finally:
    pwm0.stop()  # Stop the PWM
    pwm1.stop()
'''
pwm.change_duty_cycle(50)
pwm.change_frequency(25_000)

pwm.stop()
'''
