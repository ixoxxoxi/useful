import os
import subprocess

# 指定文件夹路径
folder_path = "/path/to/folder"

# 遍历文件夹
for root, dirs, files in os.walk(folder_path):
    for file in files:
        # 检查文件扩展名是否为.vue
        if file.endswith(".vue"):
            # 构建命令
            command = f"vtr -i {file} -o -n {os.path.splitext(file)[0]}.jsx"
            
            # 在cmd窗口执行命令
            subprocess.call(command, shell=True)
