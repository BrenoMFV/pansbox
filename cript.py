import os
from pbkdf2 import PBKDF2
from Crypto import Random
from Crypto.Cipher import AES

if __name__ == '__main__':
    key = b'Sixteen byte key'
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    msg = iv + cipher.encrypt(b'New message')
    print(msg)
