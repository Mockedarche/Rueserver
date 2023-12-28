"""
very basic client

currently handles creating account, authenticating, logout, etc
usues bcrypt to hash the password before it's sent

"""

import socket
import bcrypt

# send_string_to_server - simply takes a message and sends it to the server
def send_string_to_server(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 9999)

    try:
        client_socket.connect(server_address)
        print("Connected to the server")
        
        # Sending the string to the server
        client_socket.sendall(message.encode('ascii'))

        # Receiving the response from the server
        response = client_socket.recv(1024).decode('ascii')
        print("Server response:", response)

    except ConnectionRefusedError:
        print("Connection to the server was refused")
    finally:
        client_socket.close()


# create_account - taking the username and password get the user unique salt and hash password
# then send the hashed password to the server and have the account be created
def create_account(username, password):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 9999)

    try:
        # connect to the server
        client_socket.connect(server_address)
        print("Connected to the server")
        
        # sent our first message that we want to create an account along with the username
        message = "create_account " + username
        
        # Sending the string to the server
        client_socket.sendall(message.encode('ascii'))

        # recieve back the salt
        response = client_socket.recv(1024).decode()
        
        # attempt to hash the password with the salt
        hashed_password = bcrypt.hashpw(password.encode(), response.encode())
        command = "hashed "
        
        
        # get the hashed password read to be sent
        message = f"{command} {hashed_password}"
        
        # send that we successfully hashed the password and the hashed password
        client_socket.sendall(message.encode('ascii'))
        
        # recieve if the account was made or not
        response = client_socket.recv(1024).decode('ascii')
        print("Server response:", response)
        

    except ConnectionRefusedError:
        print("Connection to the server was refused")
    finally:
        client_socket.close()
       
# authenticate_user - takes username and password then it gets the usersalt from the server and hashes the password
# sends the has and logins the user 
def authenticate_user(username, password):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 9999)

    try:
        # connect to the server
        client_socket.connect(server_address)
        print("Connected to the server")
        
        # sent our first message that we want to create an account along with the username
        message = "authenticate " + username
        
        # Sending the string to the server
        client_socket.sendall(message.encode('ascii'))

        # recieve back the salt
        response = client_socket.recv(1024)
        
        print(str(response))
        
        # attempt to hash the password with the salt
        hashed_password = bcrypt.hashpw(password.encode(), response)
        command = "hashed "
        
        # get the hashed password read to be sent
        message = f"{command} {hashed_password}"
        
        # send that we successfully hashed the password and the hashed password
        client_socket.sendall(message.encode('ascii'))
        
        # recieve if the account was made or not
        response = client_socket.recv(1024).decode('ascii')
        print("Server response:", response)
        

    except ConnectionRefusedError:
        print("Connection to the server was refused")
    finally:
        client_socket.close()
    

# driver that takes input messages and passes them along to the server (handling commands as needed)
if __name__ == "__main__":
    while True:
            message = input("Please enter what you want to send: ")
            command, *args = message.split()  # Split the command and arguments
            # if create account or authenticate commands correctly parse input and password
            if command == "create_account":
                username = args[0]
                password = args[1]
                create_account(username, password)
            
            elif command == "authenticate":
                username = args[0]
                password = args[1]
                authenticate_user(username, password)
            else:
                send_string_to_server(message)
            
