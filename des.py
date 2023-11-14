import tables

class DES_Algorithm():

    def __init__(self, text, key, encrypt=True):
        self.text = text
        self.key = key
        self.encrypt = encrypt
        self.roundKeys = []

    def string_to_bit_array(self, text):
        res = []
        for letter in text:
            d = format(ord(letter), 'b')
            d = "0" * (8 - len(d)) + d
            res.append(d)
        return "".join(res)

    def bit_array_to_string(self, array):
        res = []
        for i in range(0, len(array), 8):
            res.append(chr(int(array[i:i + 8], 2)))
        return "".join(res)

    def permut(self, key, table):

        res = [0] * len(table)
        for index_in_result, index_in_key in enumerate(table):
            res[index_in_result] = key[index_in_key]

        return "".join(res)

    def xor(self, text, key):
        res = []
        for i, j in zip(text, key):
            if i == j:
                res.append("0")
            else:
                res.append("1")

        return "".join(res)

    def int_to_binary(self, number):

        string = str(bin(number).replace("0b", ""))
        return "0" * (4 - len(string)) + string

    def subsitution(self, key, table):
        blocks = []
        for i in range(0, len(key), 6):
            blocks.append(key[i:i + 6])
        res = []
        for index, block in enumerate(blocks):
            rowNumber = int(str(block[0]) + str(block[5]), 2)
            columnNumber = "".join(list(map(lambda x: str(x), block[1:5])))
            columnNumber = int(columnNumber, 2)
            res.append(self.int_to_binary(
                table[index][rowNumber][columnNumber]))

        return "".join(res)

    def keyGeneration(self):
        if len(self.key) < 8:
            print("La clave debe tener 8 caracteres/bits")
            exit(0)
        else:
            self.key = self.key[:8]
        shift_count = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
        key = self.string_to_bit_array(self.key)
        key = self.permut(key, tables.keyCompression64_56)
        keyLeft = key[:28]
        keyRight = key[28:]
        for count in shift_count:
            keyLeft = keyLeft[count:] + keyLeft[:count]
            keyRight = keyRight[count:] + keyRight[:count]
            self.roundKeys.append(self.permut(keyLeft + keyRight,tables.keyCompression56_48))

    def DES(self, viewSteps=False):
         
        if len(self.roundKeys) == 0:
            self.keyGeneration()

        if self.encrypt:
            keys = self.roundKeys
        else:
            keys = self.roundKeys[::-1]

        if viewSteps:
            print(f"Texto inicial: {self.text}")
            print(f"Clave secreta: {self.key}\n")

        text = self.text
        if len(text) % 8 != 0:
            text += " " * (8 - (len(text) % 8))

        result = []
        for i in range(0, len(text), 8):
            block = text[i:i + 8]
            block = self.string_to_bit_array(block)
            block = self.permut(block, tables.initialPermutation)

            for roundNumber in range(16):
                if viewSteps:
                    print(f"Round {roundNumber + 1}")
                    print(f"TextSinFormato: {hex(int(block, 2))}")
                    print(f"Key: {hex(int(keys[roundNumber]))}\n")

                blockLeft = block[:32]
                blockRight = block[32:]

                expandedRight = self.permut(
                    blockRight, tables.textExpansion32_48)

                key = self.xor(expandedRight, keys[roundNumber])

                key = self.subsitution(key, tables.subsitutionBox)
                key = self.permut(key, tables.keyShuffle)
                blockLeft = self.xor(blockLeft, key)

                blockLeft = "".join(blockLeft)
                blockLeft, blockRight = blockRight, blockLeft
                block = blockLeft + blockRight

            block = self.permut(block[32:] + block[:32],
                                tables.finalPermutation)

            if viewSteps:
                print(f"\nTexto de bloque final para ronda {roundNumber + 1}: {repr(self.bit_array_to_string(block))}\n")

            result.append(self.bit_array_to_string(block))

        result = "".join(result)

        if viewSteps:
            print(f"\nTexto Final: {repr(self.bit_array_to_string(result))}\n")

        return result


if __name__ == '__main__':
    d = DES_Algorithm("abcdeabcdeabcdeaq", "qwertyuio")
    encryptedText = d.DES(False)
    c = DES_Algorithm(encryptedText, "qwertyuio", False)
    decryptedText = c.DES(False)

    print(encryptedText)
    print(decryptedText.strip(" "))
