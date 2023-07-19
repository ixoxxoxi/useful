import os

def create_directory_tree(directory, level=0):
    tree = ""
    prefix = "|   " * level
    entries = os.listdir(directory)
    for entry in entries:
        full_path = os.path.join(directory, entry)
        if os.path.isdir(full_path):
            tree += f"{prefix}|-- {entry}\n"
            tree += create_directory_tree(full_path, level + 1)
        else:
            tree += f"{prefix}|-- {entry}\n"
    return tree

# 获取用户输入的目录路径
directory = input("请输入要遍历的目录路径：")

# 检查目录是否存在
if not os.path.isdir(directory):
    print("目录不存在！")
    exit()

tree = create_directory_tree(directory)

with open("1.txt", "w") as file:
    file.write(tree)

print("目录树已保存到1.txt文件中。")
