import os
import shutil
from cryptography.fernet import Fernet

# 生成加密密钥
def generate_key():
    password = input("请输入密码：")
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    with open('key.key', 'wb') as key_file:
        key_file.write(key)

# 加载密钥
def load_key():
    if os.path.exists('key.key'):
        with open('key.key', 'rb') as key_file:
            key = key_file.read()
        return key
    else:
        return None

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
    fernet = Fernet(key)
    with open(file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

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
    if not os.path.exists('key.key'):
        generate_key()

    key = load_key()
    if key is None:
        return

    choice = input("请选择操作：1.加密  2.解密：")
    path = input("请输入文件或文件夹路径：")

    if choice == "1":
        if os.path.isfile(path):
            encrypt_file(path, key)
            print("加密成功！")
        elif os.path.isdir(path):
            encrypt_folder(path, key)
            print("加密成功！")
    elif choice == "2":
        if os.path.isfile(path):
            decrypt_file(path, key)
            print("解密成功！")
        elif os.path.isdir(path):
            decrypt_folder(path, key)
            print("解密成功！")

if __name__ == '__main__':
    main()
