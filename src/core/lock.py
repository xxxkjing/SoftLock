import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# 从密码和盐值生成密钥
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

# 加密文件
def encrypt_file(filename: str, password: str):
    salt = os.urandom(16)  # 生成随机盐值
    key = derive_key(password, salt)
    fernet = Fernet(key)
    with open(filename, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(filename, 'wb') as encrypted_file:
        # 将盐值和密文一起写入文件
        encrypted_file.write(salt + encrypted)

# 解密文件
def decrypt_file(filename: str, password: str):
    with open(filename, 'rb') as enc_file:
        data = enc_file.read()
    salt = data[:16]  # 提取盐值
    encrypted = data[16:]  # 提取密文
    key = derive_key(password, salt)
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted)
    with open(filename, 'wb') as dec_file:
        dec_file.write(decrypted)

if __name__ == '__main__':
    password = input("请输入用于加密/解密的密码：")
    action = input("请选择操作：1. 加密文件 2. 解密文件\n")
    filename = input("请输入文件名：")
    
    if action == '1':
        encrypt_file(filename, password)
        print(f"{filename} 已加密。")
    elif action == '2':
        decrypt_file(filename, password)
        print(f"{filename} 已解密。")
    else:
        print("无效选择。")
