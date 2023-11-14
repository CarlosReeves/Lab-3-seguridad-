import socket
import time
import string
from diffie_hellman import keyGeneration, sharedKeyGeneration
from des import DES_Algorithm

serverPort = 8001
serverIP = "74.125.224.72"


def keyGenerationForDES(p, q, sharedKey):
    mapping = {}
    for index, letter in enumerate(string.ascii_letters):
        mapping[index] = letter

    val = str(sharedKey * p * q)

    finalKey = []
    for index in range(0, len(val), 2):
        finalKey.append(mapping[int(val[index:index + 1]) % len(mapping)])

    while len(finalKey) < 8:
        finalKey += finalKey

    return "".join(finalKey[:8])


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("estableciendo conexion con el cliente")
    client.connect((serverIP, serverPort))
    client.send("Connectado!".encode())
    print("Connectado!")
    
    p = int(client.recv(4096).decode())
    q = int(client.recv(4096).decode())

    print(f"Numero primo: {p}")
    print(f"Raiz: {q}\n")
    
    privateClient, publicClient = keyGeneration(p, q)
    time.sleep(2)
    
    publicServer = int(client.recv(4096).decode())

    client.send(str(publicClient).encode())

    time.sleep(2)

    key = int(str(sharedKeyGeneration(publicServer, privateClient, p)), 16)
    DES_key = keyGenerationForDES(p, q, key)

    while True:
        message_to_send = input("Tú: ")
        print("\n")
        encryptedMessage = DES_Algorithm(text=message_to_send, key=DES_key, encrypt=True).DES()
        client.send(encryptedMessage.encode())

        actual_message = client.recv(4096).decode()
        message = DES_Algorithm(text=actual_message, key=DES_key, encrypt=False).DES()
        if message != "exit":
            print("persona 2: " + message)
            print("El mensaje recibido: {0}".format(actual_message))
            print("\n")
        else:
            client.close()


if __name__ == '__main__':
    main()
