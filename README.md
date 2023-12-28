# Rueserver
This is a template for a home server idea I have. Essentially a mysql server that is connected to a server which accepts clients.

Goals - 
    This server will eventually act as a server that allows clients on MY network to add pieces to a MYSQL server.
    The goal will be for various smart devices to add data to a server where I can make a web interface to show that data.
    Currently the thinking will be pi zero w's with temperature, humidity, etc data submitting their data so I can see
    fluctuations throughout my house. Eventually i'd like to make my own humidifiers, zone cooling, etc.
    
Pre-Alpha v001
Very basic Server Client relationship right now allows clients to connect (note everything is local host right now), authenticate, create account, check if logged in,
and logout. Current bcrypt is used client side but will eventually be a server side thing as well

Next release items (don't expect these to always be so detailed) <br><br>
Password challening - In my computer security course we covered SOOOOO many ways for vulnerability when it comes to handling passwords.
One big issue was replay attacks. Hashing is great but since it's one way a client will always end up sending the same hash as their
password. One way to overcome this is to challenege the client. Essentially the client hashes like normally but is given SOMETHING
which they then hash with their hashed password. In my case it will likely be a salt. So server sends a salt so both client server now it.
Then both will hash the hashed password with that salt giving a unique hash that is sent everytime and one only the real user could know.
<br><br>
Auto logout - After x period of inactivity a client should be logged out. This will ensure after months of running my authenticated_users list
doesn't get too long. Additionally it works as a privacy measure. 
<br><br>
Tie authenticated users to a IP address - This will prevent a obvious flaw right now of bad actors posing as other clients. 
Another way could be to have a public key and private key relationship such that no bad actor could act like a real client.
