import numpy as np
from base64 import b64encode, b64decode
from utils.converter import keyToHexArray, arrayShift, arraySbox, xorArray, addRoundKey, subBytes, shiftRow, mixColumn
from utils.converter import hexToMatrix, inverseMixColumn


class AES:

    def __init__(self):
        self.ROUND = 10
        self.ORDER = 8
        self.ROUNDKEY = []

    # Key Scheduling
    def __keySchedule(self, KEY):
        ROW, COL = 8, 8
        hexKey = keyToHexArray(KEY, ROW, COL)
        self.ROUNDKEY.append(hexKey)
        #print(hexKey)
        for i in range(0, self.ROUND):
            prev_arr = self.ROUNDKEY[-1]
            last_col = prev_arr[ROW-1]
            shift_col = arrayShift(last_col)
            sbox_col = arraySbox(shift_col)
            col_1 = xorArray(prev_arr[0], sbox_col, self.ORDER, i)
            col_2 = xorArray(col_1, prev_arr[1], self.ORDER)
            col_3 = xorArray(col_2, prev_arr[2], self.ORDER)
            col_4 = xorArray(col_3, prev_arr[3])
            # additional non-linear transformation after the fourth column
            # https://crypto.stackexchange.com/questions/20/what-are-the-practical-differences-between-256-bit-192-bit-and-128-bit-aes-enc#answer-1527
            col_5 = xorArray(arraySbox(np.copy(col_4)), prev_arr[4], self.ORDER)
            col_6 = xorArray(col_5, prev_arr[5], self.ORDER)
            col_7 = xorArray(col_6, prev_arr[6], self.ORDER)
            col_8 = xorArray(col_7, prev_arr[7], self.ORDER)
            new_arr = np.array([col_1, col_2, col_3, col_4, col_5, col_6, col_7, col_8])
            self.ROUNDKEY.append(new_arr)
        self.__convertRoundKey()

    # Convert 8 4*8 Matrix to 15 4*4 Matrix
    def __convertRoundKey(self):
        self.ROUNDKEY = np.concatenate(self.ROUNDKEY)
        temp = []
        for i in range(self.ROUND+1):
            temp.append(self.ROUNDKEY[i*8:i*8+8])
        self.ROUNDKEY = temp

    # Encryption Process
    def __encryptProcess(self, TEXT):
        #print(TEXT)
        hexData = keyToHexArray(TEXT, self.ORDER, self.ORDER)
        #print(hexData)
        cipher_arr = addRoundKey(hexData, self.ROUNDKEY[0])
        for i in range(1, self.ROUND+1):
            arr = cipher_arr
            arr = subBytes(arr)
            arr = shiftRow(arr, left=True, order=self.ORDER)
            if(i != self.ROUND):
                arr = mixColumn(arr, order=self.ORDER)
            arr = addRoundKey(arr, self.ROUNDKEY[i])
            cipher_arr = arr
        return cipher_arr

    # Encryption Add Padding
    def __addPadding(self, data):
        bytes = self.ORDER**2
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
        hexData = hexToMatrix(CIPHER_HEX, self.ORDER)
        plain_arr = addRoundKey(hexData, self.ROUNDKEY[-1])
        for i in range(self.ROUND-1, -1, -1):
            arr = plain_arr
            arr = shiftRow(arr, left=False, order=self.ORDER)
            arr = subBytes(arr, inverse=True)
            arr = addRoundKey(arr, self.ROUNDKEY[i])
            if(i != 0):
                arr = inverseMixColumn(arr, order=self.ORDER)
            plain_arr = arr
        return plain_arr

    # Decryption Delete Padding
    def __delPadding(self, data):
        verify = data[-1]
        bytes = self.ORDER**2
        if(verify >= 1 and verify <= bytes-1):
            pad = data[bytes-verify:]
            sameCount = pad.count(verify)
            if(sameCount == verify):
                return data[:bytes-verify]
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
        block = self.ORDER*self.ORDER*2
        if type in ['hex', '0b', 'b64']:
            self.__keySchedule(KEY)
            data = ''

            if(type == 'b64'):
                CIPHER = b64decode(CIPHER).hex()

            if(type == '0b'):
                CIPHER = hex(int(CIPHER, 2)).replace('0x','')

            if(len(CIPHER) % block == 0 and len(CIPHER) > 0):
                examine = CIPHER
                while(len(examine) != 0):
                    plain_matrix = self.__decryptProcess(examine[:block])
                    plain_arr = list(np.array(plain_matrix).reshape(-1,))
                    plain_arr = self.__delPadding(plain_arr)
                    for j in plain_arr:
                        data+=chr(j)
                    if(len(examine)==block):
                        examine=''
                    else:
                        examine=examine[block:]
                self.ROUNDKEY = []
                return data

            else:
                raise Exception(f"Hex: {CIPHER}, should be non-empty multiple of 32bits")

        else:
            raise Exception(f"type := ['hex', '0b', 'b64'] but got '{type}'")
        

if(__name__ == '__main__'):

    aes512 = AES()

    key = 'Thats my Kung Fu1234567876543210Thats my Kung Fu1234567876543210'
    msg = 'Checking AES 512 on Python'
    encode = '__all__'      # hex, b64 => base64, 0b => binary

    x = aes512.encrypt(key, msg, encode)
    print(x)

    # # decode from binary
    y = aes512.decrypt('Thats my Kung Fu1234567876543210Thats my Kung Fu1234567876543210', x['0b'], '0b')     
    print(y)