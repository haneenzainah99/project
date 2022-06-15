import random
from socket import *
from generate_key import generate_key
from cryptography.fernet import Fernet

client = socket(AF_INET,SOCK_STREAM)

client.connect(("127.0.0.1", 2222))

while True:
    G = 9
    P = 23
    
    b = random.randint(10,100)
    print("b=", b)
    y = int(pow(G, b, P))
    print("y=", y)
    x = int(client.recv(1024).decode())
    print("x=", x)
    salt = client.recv(1024)
    print("salt=", salt)
    
    client.send(str(y).encode())
    k = int(pow(x, b, P))
    print("k=", k)
    password = str(k).encode()
    
    key = generate_key(password, salt)
    print("key=", key)
    fernet = Fernet(key)
    
    while True:
        message = input("Enter a message: ")
        enc_message = fernet.encrypt(message.encode())
        print(">> {} [{}]".format(message, enc_message.decode()))
        client.send(enc_message)

        r_enc_message = client.recv(1024)
        r_message = fernet.decrypt(r_enc_message).decode()
        print("<< {} [{}]".format(r_message, r_enc_message.decode()))

