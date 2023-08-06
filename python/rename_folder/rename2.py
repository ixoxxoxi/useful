import os

def rename_files(folder_path):
    renamed_files = []  # 存储已重命名的文件名
    
    # 遍历文件夹下的所有文件和文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isdir(file_path):
                continue
            file_name_without_extension = os.path.splitext(file)[0]
            if len(file_name_without_extension) < 3:
                # 获取当前文件所在目录的名字
                directory_name = os.path.basename(root)
                # 拼接新文件名
                new_file_name = f"{directory_name}-{file}"
                # 重命名文件
                new_file_path = os.path.join(root, new_file_name)
                os.rename(file_path, new_file_path)
                renamed_files.append((file, new_file_name))
    
    # 输出已完成重命名的文件名
    if len(renamed_files) > 0:
        print("以下文件已完成重命名：")
        for old_name, new_name in renamed_files:
            print(f"{old_name} -> {new_name}")
    else:
        print("没有满足重命名条件的文件。")

def main():
    # 询问需要遍历的文件夹路径
    folder_path = input("请输入要遍历的文件夹路径：")
    
    # 验证文件夹路径的有效性
    if not os.path.isdir(folder_path):
        print("无效的文件夹路径！")
        return
    
    # 调用函数
    rename_files(folder_path)

# 调用主函数
main()
