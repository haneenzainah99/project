import random
import string
from socket import *
from threading import Thread
from generate_key import generate_key
from cryptography.fernet import Fernet

server = socket(AF_INET,SOCK_STREAM)

server.bind(("127.0.0.1", 2222))

server.listen()

print('Starting server..')

def worker(client):
    G = 9
    P = 23
    
    a = random.randint(10,100)
    print("a=", a)
    x = int(pow(G, a, P))
    print("x=", x)
    salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)).encode()
    print("salt=", salt)
    client.send(str(x).encode())
    client.send(salt)
    
    y = int(client.recv(1024).decode())
    print("y=", y)
    
    k = int(pow(y, a, P))
    print("k=", k)
    password = str(k).encode()
    
    key = generate_key(password, salt)
    print("key=", key)
    fernet = Fernet(key)
    
    while True:
        enc_message = client.recv(1024)
        message = fernet.decrypt(enc_message).decode()
        print("<< {} [{}]".format(message, enc_message.decode()))
        message=message[::-1]
        enc_message = fernet.encrypt(message.encode())
        print(">> {} [{}]".format(message, enc_message.decode()))
        client.send(enc_message)

while True:
    client, remote_address = server.accept()
    print('Receive connection from address: ', remote_address)

    thread = Thread(target=worker, args=(client,))
    thread.start()

