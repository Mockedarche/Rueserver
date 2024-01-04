
"""
very basic sensor script

goal will eventually be to handle various sensor type data

"""

import socket
import network

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect('ssid', 'password')
    while not sta_if.isconnected():
        pass
print('network config:', sta_if.ifconfig())

def sensor(username, type_of_sensor, ip, port, data):
    if type_of_sensor == "temp/humidity":
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (ip, port)

        try:
            # connect to the server
            client_socket.connect(server_address)
            print("Connected to the server")

            message = "sensor temp temp/humidity 85f 40\% humidity"

            client_socket.sendall(message.encode("ascii"))

            response = client_socket.recv(1024)

            print(response)

        except ConnectionRefusedError:
            print("Connection to the server was refused")
        finally:
            client_socket.close()

# driver that takes input messages and passes them along to the server (handling commands as needed)
if __name__ == "__main__":
    ip = input("Enter IP address: ")
    port = int(input("Enter port: "))

    while True:
        message = input("Please enter what you want to send: ")
        command, *args = message.split()  # Split the command and arguments
        if command == "sensor":
            sensor("test", "temp/humidity", ip, port, "temp")
        else:
            send_string_to_server(message, ip, port)
            

