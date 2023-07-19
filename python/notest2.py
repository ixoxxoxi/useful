import os
import subprocess

def execute_command(file_path):
    # 构建命令
    command = f'vtr -i {file_path} -o -n {os.path.splitext(file_path)[0]}.jsx'
    # 执行命令
    subprocess.call(command, shell=True)

def traverse_folders(folder_path):
    # 遍历文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 检查文件扩展名是否为.vue
            if file.endswith('.vue'):
                file_path = os.path.join(root, file)
                # 执行命令
                execute_command(file_path)

# 指定文件夹路径
folder_path = '指定文件夹路径'
# 遍历文件夹并执行命令
traverse_folders(folder_path)