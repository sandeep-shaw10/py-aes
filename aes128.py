import numpy as np
from base64 import b64encode, b64decode
from utils.converter import keyToHexArray, arrayShift, arraySbox, xorArray, addRoundKey, subBytes, shiftRow, mixColumn
from utils.converter import hexToMatrix, inverseMixColumn


class AES:

    def __init__(self):
        self.ROUND = 10
        self.ORDER = 4
        self.ROUNDKEY = []

    # Key Scheduling
    def __keySchedule(self, KEY):
        hexKey = keyToHexArray(KEY)
        self.ROUNDKEY.append(hexKey)
        for i in range(0, self.ROUND):
            prev_arr = self.ROUNDKEY[-1]
            last_col = prev_arr[self.ORDER-1]
            shift_col = arrayShift(last_col)
            sbox_col = arraySbox(shift_col)
            col_1 = xorArray(prev_arr[0], sbox_col, i)
            col_2 = xorArray(col_1, prev_arr[1])
            col_3 = xorArray(col_2, prev_arr[2])
            col_4 = xorArray(col_3, prev_arr[3])
            new_arr = np.array([col_1, col_2, col_3, col_4])
            self.ROUNDKEY.append(new_arr)

    # Encryption Process
    def __encryptProcess(self, TEXT):
        hexData = keyToHexArray(TEXT)
        cipher_arr = addRoundKey(hexData, self.ROUNDKEY[0])
        for i in range(1, self.ROUND+1):
            arr = cipher_arr
            arr = subBytes(arr)
            arr = shiftRow(arr)
            if(i != self.ROUND):
                arr = mixColumn(arr)
            arr = addRoundKey(arr, self.ROUNDKEY[i])
            cipher_arr = arr
        return cipher_arr

    # Encryption Add Padding
    def __addPadding(self, data):
        bytes = 16
        bits_arr = []
        while(True):
            if(len(data) > bytes):
                bits_arr.append(data[:bytes])
                data = data[bytes:]
            else:
                space = bytes-len(data)
                bits_arr.append(data + chr(space)*space)
                break
        return bits_arr

    # Decryption Process
    def __decryptProcess(self, CIPHER_HEX):
        hexData = hexToMatrix(CIPHER_HEX)
        plain_arr = addRoundKey(hexData, self.ROUNDKEY[-1])
        for i in range(self.ROUND-1, -1, -1):
            arr = plain_arr
            arr = shiftRow(arr, left=False)
            arr = subBytes(arr, inverse=True)
            arr = addRoundKey(arr, self.ROUNDKEY[i])
            if(i != 0):
                arr = inverseMixColumn(arr)
            plain_arr = arr
        return plain_arr

    # Decryption Delete Padding
    def __delPadding(self, data):
        verify = data[-1]
        if(verify >= 1 and verify <= 15):
            pad = data[16-verify:]
            sameCount = pad.count(verify)
            if(sameCount == verify):
                return data[:16-verify]
            return data
        return data

    #Encryption
    def encrypt(self, KEY, TEXT, type='hex'):
        text_arr = self.__addPadding(TEXT)
        self.__keySchedule(KEY)
        hex_ecrypt=''
        for i in text_arr:
            cipher_matrix = self.__encryptProcess(i)
            cipher_text = list(np.array(cipher_matrix).reshape(-1,))
            for j in cipher_text:
                hex_ecrypt+=f'{j:02x}'
        self.ROUNDKEY = []
        #conversion
        if(type == 'b64'):
            return b64encode(bytes.fromhex(hex_ecrypt)).decode()
        if(type == '0b'):
            return f'{int(hex_ecrypt, 16):0>b}'
        if(type == '__all__'):
            return {
                'hex': hex_ecrypt,
                'b64': b64encode(bytes.fromhex(hex_ecrypt)).decode(),
                '0b': bin(int(hex_ecrypt, 16))[2:].zfill(len(hex_ecrypt) * 4)
            }
        return hex_ecrypt

    # Decryption
    def decrypt(self, KEY, CIPHER, type='hex'):
        if type in ['hex', '0b', 'b64']:
            self.__keySchedule(KEY)
            data = ''

            if(type == 'b64'):
                CIPHER = b64decode(CIPHER).hex()

            if(type == '0b'):
                CIPHER = hex(int(CIPHER, 2)).replace('0x','')

            if(len(CIPHER) % 32 == 0 and len(CIPHER) > 0):
                examine = CIPHER
                while(len(examine) != 0):
                    plain_matrix = self.__decryptProcess(examine[:32])
                    plain_arr = list(np.array(plain_matrix).reshape(-1,))
                    plain_arr = self.__delPadding(plain_arr)
                    for j in plain_arr:
                        data+=chr(j)
                    if(len(examine)==32):
                        examine=''
                    else:
                        examine=examine[32:]
                self.ROUNDKEY = []
                return data

            else:
                raise Exception(f"Hex: {CIPHER}, should be non-empty multiple of 32bits")

        else:
            raise Exception(f"type := ['hex', '0b', 'b64'] but got '{type}'")


if(__name__ == '__main__'):

    aes128 = AES()

    key = 'Thats my Kung Fu'
    msg = 'Checking AES 128 on Python'
    encode = '__all__'      # hex, b64 => base64, 0b => binary

    x = aes128.encrypt(key, msg, encode)
    print(x)

    # decode from binary
    y = aes128.decrypt(key, x['0b'], '0b')     
    print(y)

    # decode from base64
    y = aes128.decrypt(key, x['b64'], 'b64')
    print(y)

    # decode from hex (default)
    y = aes128.decrypt(key, x['hex'])
    print(y)