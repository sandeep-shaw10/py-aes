# Advance Encryption Standard

<div style='display: flex'>

<div style='margin: 1%'>

![py](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=gray)

</div>
<div style='margin: 1%'>

![num-py](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)

</div>
<div style='margin: 1%'>

![num-py](https://img.shields.io/badge/base64-f75cd8?style=for-the-badge&logo=python&logoColor=white)

</div>

</div>
<div style='display: flex'>
<div style='margin: 1%'>

[![Generic badge](https://img.shields.io/badge/AES-128-ed7c31.svg)](./aes128.py)

</div>
<div style='margin: 1%'>

[![Generic badge](https://img.shields.io/badge/AES-192-00b04f.svg)](./aes192.py)

</div>
<div style='margin: 1%'>

[![Generic badge](https://img.shields.io/badge/AES-256-00b0f0?.svg)](./aes256.py)

</div>

</div>

### Key Schedule

```py
# ROUNDKEY := []
# hexKey := keyToHexArray(KEY)
# ROUNDKEY.append(hexKey)
# LOOP => 1 to ORDER
    # arr := Fetch last array of roundkey
    # xc := last row of arr
    # sc := shift row / ROTWORD 
    # s-box-row := S_box(sc)
    # a := XOR row-1,s-box-row,rcon-1
    # b := XOR a,row-2
    # c := XOR b,row-3
    # d := XOR c,row-4
    # x := matrix [a,b,c,d]
    # append x to ROUNDKEY
```

### Example
Round Key: [Detailed Example](https://www.kavaliro.com/wp-content/uploads/2014/03/AES.pdf).

Key: 'Thats my Kung Fu' => hex(54 68 61 74 73 20 6D 79 20 4B 75 6E 67 20 46 75)
- `Round 0:` 54 68 61 74 73 20 6D 79 20 4B 75 6E 67 20 46 75
- `Round 1:` E2 32 FC F1 91 12 91 88 B1 59 E4 E6 D6 79 A2 93
- `Round 2:` 56 08 20 07 C7 1A B1 8F 76 43 55 69 A0 3A F7 FA
- `Round 3:` D2 60 0D E7 15 7A BC 68 63 39 E9 01 C3 03 1E FB
- `Round 4:` A1 12 02 C9 B4 68 BE A1 D7 51 57 A0 14 52 49 5B
- `Round 5:` B1 29 3B 33 05 41 85 92 D2 10 D2 32 C6 42 9B 69
- `Round 6:` BD 3D C2 B7 B8 7C 47 15 6A 6C 95 27 AC 2E 0E 4E
- `Round 7:` CC 96 ED 16 74 EA AA 03 1E 86 3F 24 B2 A8 31 6A
- `Round 8:` 8E 51 EF 21 FA BB 45 22 E4 3D 7A 06 56 95 4B 6C
- `Round 9:` BF E2 BF 90 45 59 FA B2 A1 64 80 B4 F7 F1 CB D8
- `Round 10:` 28 FD DE F8 6D A4 24 4A CC C0 A4 FE 3B 31 6F 26

![wikipedia algorithm](./resources/1.png)

Key Schedule: [Wikipedia](https://en.wikipedia.org/wiki/AES_key_schedule)

# `Rounds` & `Keys`

![aes-128](./resources/2.png)
![aes-128](./resources/3.png)
![aes-128](./resources/4.png)

# Encryption Process

```py
# cipher_arr := []

# Round 0
    # data_arr := dataToHexArray(data)
    # cipher_arr := XOR(data_arr, ROUNDKEY[0])

# Round [i] from 1 to 10
    # arr := prev_arr
    # arr := sBox(arr)
    # arr := shiftRow(arr)
    # arr := mixColumn(arr)     <<Skip for last round>>
    # key_arr := ROUNDKEY[i]
    # xor_arr := XOR(data_arr, key_arr)

# return cipher_arr
```

# Decryption Process

```py
# plain_arr := []

# Round 0
    # data_arr := dataToHexArray(data)
    # plain_arr := XOR(data_arr, ROUNDKEY[0])

# Round [i] from 1 to 10
    # arr := prev_arr
    # arr := shiftRow(arr)
    # arr := sBox(arr)
    # key_arr := ROUNDKEY[10-i]
    # xor_arr := XOR(data_arr, key_arr)
    # arr := mixColumn(arr)     <<Skip for last round>>

# return plain_arr
```



# Using AES-128/192/256

`index.py`

```py
from aes128 import AES as AES_128
from aes192 import AES as AES_192
from aes256 import AES as AES_256


msg = 'Checking AES Encryption & Decryption on python'
encode = '__all__'  #hex, base64, binary


print('AES 128')
key = 'Thats my Kung Fu'    # 16 character / 128 bits
encrypt_128 = AES_128()
x = encrypt_128.encrypt(key, msg, encode)
y = encrypt_128.decrypt(key, x['hex'])
print(x)
print(y, end='\n\n')


print('AES 192')
key = 'Thats my Kung Fu Panda !'    # 24 character / 192 bits
encrypt_192 = AES_192()
x = encrypt_192.encrypt(key, msg, encode)
y = encrypt_192.decrypt(key, x['hex'])
print(x)
print(y, end='\n\n')


print('AES 256')
key = 'Thats my Kung Fu Panda ! Style12'    # 32 character / 256 bits
encrypt_256 = AES_256()
x = encrypt_256.encrypt(key, msg, encode)
y = encrypt_256.decrypt(key, x['hex'])
print(x)
print(y, end='\n\n')
```

`Create Virtual Environment`

```cmd
py -m venv venv-aes
```

`Activate Virtual Environment`

```cmd
source venv-aes/Scripts/activate
```

`Install Dependencies`

```cmd
pip install -r requirements.txt
```

`Run`

```cmd
py index.py
```

`Output`

```json
AES 128
{
    "hex":"d4c31bf63ef0bd1379ddf17d21d4719c668abac96f00319005fe876061b75e02dfeeb3d359f39a1d73e049f91ed53388", 
    "b64":"1MMb9j7wvRN53fF9IdRxnGaKuslvADGQBf6HYGG3XgLf7rPTWfOaHXPgSfke1TOI",
    "0b":"110101001100001100011011111101100011111011110000101111010001001101111001110111011111000101111101001000011101010001110001100111000110011010001010101110101100100101101111000000000011000110010000000001011111111010000111011000000110000110110111010111100000001011011111111011101011001111010011010110011111001110011010000111010111001111100000010010011111100100011110110101010011001110001000"
}        
Checking AES Encryption & Decryption on python

AES 192
{
    "hex":"9210311b471c154ec96e5bfaf55e14e11aa3ee0431ffedcc13457fe0650c47c60525d65dc934cecd62ca51b3e59de8c3", 
    "b64": "khAxG0ccFU7Jblv69V4U4Rqj7gQx/+3ME0V4GUMR8YFJdZdyTTOzWLKUbPlnejD", 
    "0b": "100100100001000000110001000110110100011100011100000101010100111011001001011011100101101111111010111101010101111000010100111000010001101010100011111011100000010000110001111111111110110111001100000100110100010101111111111000000110010100001100010001111100011000000101001001011101011001011101110010010011010011001110110011010110001011001010010100011011001111100101100111011110100011000011"
}        
Checking AES Encryption & Decryption on python

AES 256
{
    "hex": "2fbdbe08951833c21295adfdb0878ac4170b2d62106dfe7d0978cb61819c74623a3b5872135170ee2d4b48001b5eb8a3", 
    "b64": "L72+CJUYM8ISla39sIeKxBcLLWIQbf59CXjLYYGcdGI6O1hyE1Fw7i1LSAAbXrij", 
    "0b": "001011111011110110111110000010001001010100011000001100111100001000010010100101011010110111111101101100001000011110001010110001000001011100001011001011010110001000010000011011011111111001111101000010010111100011001011011000011000000110011100011101000110001000111010001110110101100001110010000100110101000101110000111011100010110101001011010010000000000000011011010111101011100010100011"
}        
Checking AES Encryption & Decryption on python
```