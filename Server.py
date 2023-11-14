import socket
import time
import string
from diffie_hellman import getLargePrimeNumber, getPrimitiveRoot, keyGeneration, sharedKeyGeneration
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
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((serverIP, serverPort))
    server.listen(1)

    print("Establecimiento de conexión")
    client_sock, address = server.accept()
    print(client_sock.recv(4096).decode())

    p = getLargePrimeNumber(1000, 2000)
    q = getPrimitiveRoot(p, True)

    print("Reenvío de parámetros globales")
    client_sock.send(str(p).encode())
    time.sleep(2)
    client_sock.send(str(q).encode())

    privateServer, publicServer = keyGeneration(p, q)
    time.sleep(2)
    client_sock.send(str(publicServer).encode())

    publicClient = int(client_sock.recv(4096).decode())

    time.sleep(2)

    key = int(str(sharedKeyGeneration(publicClient, privateServer, p)), 16)
    DES_key = keyGenerationForDES(p, q, key)

    while True:
        actual_message = client_sock.recv(4096).decode()
        message = DES_Algorithm(text=actual_message,
                                key=DES_key, encrypt=False).DES()
        if message != "exit":
            print("cliente dice: " + message)
            print("El mensaje recibido: {0}".format(actual_message))
            message_to_send = input("Tú: ")
            encrytedMessage = DES_Algorithm(
                text=message_to_send, key=DES_key, encrypt=True).DES()
            client_sock.send(encrytedMessage.encode())
        else:
            client_sock.close()


if __name__ == '__main__':
    main()
