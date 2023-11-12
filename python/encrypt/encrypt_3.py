import os
import shutil
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

# 生成加密密钥
def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

# 加密文件
def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        original_data = file.read()
    encrypted_data = fernet.encrypt(original_data)
    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

# 解密文件
def decrypt_file(file_path, key):
    try:
        fernet = Fernet(key)
        with open(file_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()
        decrypted_data = fernet.decrypt(encrypted_data)
        with open(file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)
    except Exception as e:
        print("解密失败！密码错误或无效的文件。")

# 加密文件夹
def encrypt_folder(folder_path, key):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key)

# 解密文件夹
def decrypt_folder(folder_path, key):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            decrypt_file(file_path, key)

# 主程序
def main():
    choice = input("请选择操作：1.加密  2.解密：")
    path = input("请输入文件或文件夹路径：")
    password = input("请输入主密码：")
    salt = input("请输入副密码：")

    key = generate_key(password, salt.encode())

    if choice == "1":
        if os.path.isfile(path):
            encrypt_file(path, key)
            print("加密成功！")
        elif os.path.isdir(path):
            encrypt_folder(path, key)
            print("加密成功！")
        else:
            print("无效的文件或文件夹路径！")
    elif choice == "2":
        if os.path.isfile(path):
            decrypt_file(path, key)
            print("解密成功！")
        elif os.path.isdir(path):
            decrypt_folder(path, key)
            print("解密成功！")
        else:
            print("无效的文件或文件夹路径！")

if __name__ == '__main__':
    main()
