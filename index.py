from aes128 import AES as AES_128
from aes192 import AES as AES_192
from aes256 import AES as AES_256


msg = 'Checking AES Encryption & Decryption on python'
encode = '__all__'


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