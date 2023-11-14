import random

def ObtenerNumPrimo(lowerLimit, upperLimit):
    p = 2
    upperLimit = max(upperLimit, 2)
    Primo = [False] * 2 + [True] * (upperLimit - 1)
    while (p ** 2 < upperLimit):
        if Primo[p]:
            for i in range(p ** 2, upperLimit + 1, p):
                Primo[i] = False

        p += 1

    result = [i for i, check in enumerate(Primo) if check and i > lowerLimit]
    return random.choice(result)


def ObtenerRaizPrim(q, reverse=False):
    if Primo(q):
        test = set()
        pos = [x for x in range(2, q)]
        if reverse:
            pos = pos[::-1]

        for num in pos:
            for i in range(1, q):
                val = (num ** i) % q
                if val in test:
                    test = set()
                    break
                else:
                    test.add(val)

                if len(test) == q - 1:
                    return num
    else:
        print("El número ingresado no es primo: Sin raíz primitiva")
        return None


def keyGeneration(number, root, privateKeyLimit=101):
    privateKeyLimit = max(privateKeyLimit, 101)
    private = random.randint(privateKeyLimit - 100, privateKeyLimit)
    public = (root ** private) % number
    return (private, public)


def sharedKeyGeneration(publicKey, privateKey, number):
    return (publicKey ** privateKey) % number


def Primo(number):
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False

    return True


if __name__ == '__main__':
    print("Esta es solo una colección de funciones necesarias para la implementación de intercambio de claves Diffie-Hellman")
