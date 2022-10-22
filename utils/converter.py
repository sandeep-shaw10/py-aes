import numpy as np
from utils.constant import s_box, roundConstant, encryptMDS, mc2, mc3
from utils.constant import invs_box, decryptMDS, mc9, mc11, mc13, mc14


# Key to Matrix
def keyToHexArray(key, row=4, col=4):
    arr = []
    for i in key:
        arr.append(ord(i))
    arr = np.array(arr)
    arr = arr.reshape(row,col)    # 4*4 matrix
    return arr


# Apply left shift / RotWord
def arrayShift(arr, shift=-1):
    return np.roll(arr, shift)


# S-box on 1D Array
def arraySbox(arr):
    for i in range(0, len(arr)):
        lsb = arr[i] & 0b00001111
        msb = (arr[i] & 0b11110000) >> 4
        arr[i] = s_box[msb, lsb]
    return arr
    

# Inverse S-box on 1D Array
def arrayInvSbox(arr):
    for i in range(0, len(arr)):
        lsb = arr[i] & 0b00001111
        msb = (arr[i] & 0b11110000) >> 4
        arr[i] = invs_box[msb, lsb]
    return arr


# XOR Operation on [arr1, arr2] or [arr1,arr2,rcon(i)]
def xorArray(arr1, arr2, rcon=-1):
    xor_arr = []
    if(arr1.shape == arr2.shape and (rcon >= -1 and rcon <= 9)):
        if(rcon == -1):
            for i in range(len(arr1)):
                val = arr1[i] ^ arr2[i]
                xor_arr.append(val)
        else:
            rcon_arr = roundConstant[rcon]
            for i in range(len(arr1)):
                val = arr1[i] ^ arr2[i] ^ rcon_arr[i]
                xor_arr.append(val)
        xor_arr = np.array(xor_arr)
        return xor_arr
    else:
        print('Array must be same dimension numpy OR Rcon: roundconstant must be 0-10')
        print(arr1, arr2, rcon)
        return False


# Xor 2 2D array
def addRoundKey(arr1, arr2):
    return np.bitwise_xor(arr1, arr2)


# Substitution-box on 2D Array
def subBytes(arr, inverse=False):
    for i in arr:
        if(not inverse):
            arraySbox(i)
        else:
            arrayInvSbox(i)
    return arr


# Shift Row on 2D Array
def shiftRow(arr, left=True, order=4):
    shifted_arr = []
    for i in range(0, order):
        if(left):
            x = arrayShift(arr[:,i],-1*i)   #Left circular shift: Encryption
        else:
            x = arrayShift(arr[:,i],i)    #Right circular shift: Decryption
        shifted_arr.append(x)
    shifted_arr = np.array(shifted_arr)     # Accurate
    return np.transpose(shifted_arr)


# Mix Column
def mixColumn(arr, order=4):
    arr = np.transpose(arr)
    mix_arr = np.zeros((order, order), dtype=int)
    for i in range(0, order):
        for j in range(0, order):
            for k in range(0, order):
                if(encryptMDS[i][k] == 1):
                    mix_arr[i][j] ^= arr[k][j]
                lsb = arr[k][j] & 0b00001111
                msb = (arr[k][j] & 0b11110000) >> 4
                if(encryptMDS[i][k] == 2):
                    mix_arr[i][j] ^= mc2[msb,lsb]
                if(encryptMDS[i][k] == 3):
                    mix_arr[i][j] ^= mc3[msb,lsb]
    return np.transpose(mix_arr)


# Inverse Mix Column
def inverseMixColumn(arr, order=4):
    arr = np.transpose(arr)
    mix_arr = np.zeros((order, order), dtype=int)
    for i in range(0, order):
        for j in range(0, order):
            for k in range(0, order):
                lsb = arr[k][j] & 0b00001111
                msb = (arr[k][j] & 0b11110000) >> 4
                if(decryptMDS[i][k] == 9):
                    mix_arr[i][j] ^= mc9[msb,lsb]
                if(decryptMDS[i][k] == 11):
                    mix_arr[i][j] ^= mc11[msb,lsb]
                if(decryptMDS[i][k] == 13):
                    mix_arr[i][j] ^= mc13[msb,lsb]
                if(decryptMDS[i][k] == 14):
                    mix_arr[i][j] ^= mc14[msb,lsb]
    return np.transpose(mix_arr)



# Decryption: ecrypted hex to matrix
def hexToMatrix(data, order=4, hexbit=32):
    if(len(data) == hexbit):
        val = [data[i:i+2] for i in range(0, len(data), 2)]
        val = [int(x,16) for x in val]
        arr = np.array(val)
        arr = arr.reshape(order,order)    # 4*4 matrix
        return arr
    else:
        print('length of encrypted data should be 32')