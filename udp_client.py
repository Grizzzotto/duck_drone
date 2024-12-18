# UDP Client
import pygame
import socket
import time
import random

#pygame init start
#joystick init
joystick_enable = 0
try:
    pygame.joystick.init()
    joystick = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())] #joystick init
    axis_0 = pygame.joystick.Joystick(0).get_axis(0) #reading information from joystick
    joystick_enable = 1
    axis_0 = 0
    axis_1 = -1
except:
    print('joystick is not defined')

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((150,200))

#pygame init end


# Client settings
SERVER_ADDRESS = "192.168.0.106"
SERVER_ADDRESS2 = "192.168.0.109"
SERVER_PORT = 12345
pps = 0.1    # Seconds to next package

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        if joystick_enable == 1: # init
            axis_0 = pygame.joystick.Joystick(0).get_axis(0)
            if pygame.joystick.Joystick(0).get_button(5):
                print("key 5 down")
                axis_1 = pygame.joystick.Joystick(0).get_axis(2)
                print(axis_1)
            else:
                axis_1 = 1
        else:
            axis_0 = 0
            axis_1 = 0
        servo = int(150 + axis_0*50)
        throttle = int(150 - axis_1*50)
        numbers = [servo, throttle]
        message = ",".join(map(str, numbers))
        # Sending packages to server
        client_socket.sendto(message.encode(), (SERVER_ADDRESS, SERVER_PORT))
        client_socket.sendto(message.encode(), (SERVER_ADDRESS2, SERVER_PORT))
        print(f"Sent: {numbers}")
        time.sleep(pps)

        screen.fill((240, 240, 240))
        # pygame.draw.rect(screen, "green", (x_throttle, y_throttle, 50, 50))

        pygame.display.update()
        clock.tick(120)
except KeyboardInterrupt:
    print("\nClient stopped")
finally:
    client_socket.close()