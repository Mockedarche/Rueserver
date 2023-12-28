"""
Very basic server 
right now allows clients to connect (note everything is local host right now), authenticate, create account, check if logged in,
and logout. Current bcrypt is used client side but will eventually be a server side thing as well

Goals - 
    This server will eventually act as a server that allows clients on MY network to add pieces to a MYSQL server.
    The goal will be for various smart devices to add data to a server where I can make a web interface to show that data.
    Currently the thinking will be pi zero w's with temperature, humidity, etc data submitting their data so I can see
    fluctuations throughout my house. Eventually i'd like to make my own humidifiers, zone cooling, etc.
    
Pre-Alpha v001
Very basic Server Client relationship right now allows clients to connect (note everything is local host right now), authenticate, create account, check if logged in,
and logout. Current bcrypt is used client side but will eventually be a server side thing as well

Next release items (don't expect these to always be so detailed)
Password challening - In my computer security course we covered SOOOOO many ways for vulnerability when it comes to handling passwords.
One big issue was replay attacks. Hashing is great but since it's one way a client will always end up sending the same hash as their
password. One way to overcome this is to challenege the client. Essentially the client hashes like normally but is given SOMETHING
which they then hash with their hashed password. In my case it will likely be a salt. So server sends a salt so both client server now it.
Then both will hash the hashed password with that salt giving a unique hash that is sent everytime and one only the real user could know.

Auto logout - After x period of inactivity a client should be logged out. This will ensure after months of running my authenticated_users list
doesn't get too long. Additionally it works as a privacy measure. 

Tie authenticated users to a IP address - This will prevent a obvious flaw right now of bad actors posing as other clients. 
Another way could be to have a public key and private key relationship such that no bad actor could act like a real client.

"""

import mysql.connector
import socket
import bcrypt

# dictionary for login information and a list to keep track of users that have been authenticated
login_info = dict()
authenticated_users = []

# simple function that reads in the login information to the dictionary
def read_in_logins():
    with open('definitely_not_logins.txt', 'r') as file:
        for line in file:
            line = line.strip()
            username, password, salt = line.split(":", 2)
            login_info[username] = (password, salt.encode())
            
# authenticate_login checks the given password to what's on file
# TODO add a challenege in order to prevent replay attacks
def authenticate_login(username, client_socket, client_address):
    print("Attempting to authenticate user")
    
    client_socket.sendall(login_info[username][1])
    print(login_info[username][1])
    
    # get backed if hashed worked and the hashed password
    message = client_socket.recv(1024).decode('ascii').split()
    
    if message[0] == "hashed":
        if str(message[1]) == login_info[username][0]:
            print("Successfully authenticated user: " + str(username))
            new_user = {"username": username, "ip_address": client_address}
            print(new_user)
            authenticated_users.append(new_user)
            return "Success"
        else:
            print("Failed to authenticate user: " + str(username))
            return "Failed"
    else:
        return "Failed"
            
    
# is_user_authenticated checks if the user has been logged in
def is_user_authenticated(username, client_address):
    for user in authenticated_users:
        if user['username'] == username and user['ip_address'] == client_address:
            print(user)
            print("User: " + str(username) + " is loggged in")
            return "Success"
    
    
    print("User: " + str(username) + " is NOT loggged in")
    return "Failed"

# create_user simple takes the given username and (should be hashed) password and adds them to our dictionary and list
# TODO verify that the password has been correctly hashed
def create_user(username, client_socket):
    print("Attempting to create user")
    
    # TODO add a check if it's already in the login
    if username in login_info:
        return "Failed to create account"
    else:
        # generate salt
        salt = bcrypt.gensalt()
    
        # send the user unique salt
        client_socket.sendall(salt)
    
        # get backed if hashed worked and the hashed password
        message = client_socket.recv(1024).decode('ascii').split()
    
        # if the hash went through then we have created our user account
        if message[0] == "hashed":
            # print out that the account was created and then add the user to the dictionary and file
            print("Successfully created user: " + str(username))
            login_info[username] = (message[1], salt)
            with open('definitely_not_logins.txt', 'a') as file:
                file.write(str(username) + ":" + str(message[1]) + ":" + salt.decode() + '\n')
    
            return "Success"
            
        else:
            return "Failed to create account"

# logout_user removes the user from the authenticated_users
# NOTE eventually gonna add a timeout function so if a client hasn't messaged in awhile it's logged out
def logout_user(username):
    print("Attempting to logout user: " + str(username))
    if username in authenticated_users:
        print("Successfully logged out user: " + str(username))
        authenticated_users.remove(username)
    else:
        print("User wasn't logged in")


# for future use will be used so that clients can add stuff to the MYSQL server
"""
try:
    
    print("Attempting to connect to the server")
    # Make a connection to the mysql server using HARDCODED authenication details
    connection = mysql.connector.connect(user='root', password="TEMPFORUPLOAD",
                                  host='127.0.0.1', database="tempDataBase")

    if connection.is_connected():
        print("Connected to MySQL database")

except mysql.connector.Error as e:
    print("Error connecting to MySQL:", e)

finally:
    # Close the connection
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("MySQL connection is closed")
   
   
"""
             
# Pseudo server to handle client connections
def run_server():
    # set up our listening connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9999))
    server_socket.listen(5)
    print("Server listening for incoming connections...")

    # while true keep running the server
    while True:
            # wait for a client to connect 
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")

            # Receive the command from the client
            message = client_socket.recv(1024).decode('ascii').split()
            # the first string (space delimited) should indicate the command
            command = message[0]

            # see what commands where sent such as authenticate, create_account, etc
            if command == "authenticate":
                username = message[1]
                response = authenticate_login(username, client_socket, client_address)
                client_socket.sendall(response.encode('ascii'))
            # Add more conditions for other commands
            elif command == "create_account":
                username = message[1]
                response = create_user(username, client_socket)
                client_socket.sendall(response.encode('ascii'))
            # client_socket.close()
            elif command == "am_authenticated":
                username = message[1]
                response = is_user_authenticated(username, client_address)
                client_socket.sendall(response.encode('ascii'))
            # if a invalid command was sent print out what command was sent and the clients IP (for future debugging)
            else:
                print(command)
                print("Invalid command was sent to the Server by IP: " + str(client_address[0]))
                
            # close the connection
            client_socket.close()

# driver that sets up logins and runs the server
if __name__ == "__main__":
    read_in_logins()
    run_server()
    
    
    
    
    
    
    
    