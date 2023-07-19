import os

def create_directory_tree(directory, file):
    file.write(f"{directory}\n")
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            file.write("|-- " + item + "\n")
            create_directory_tree(item_path, file)
        else:
            file.write("|   |-- " + item + "\n")

def main():
    directory = input("请输入要遍历的目录路径：")
    if not os.path.exists(directory):
        print("目录不存在，请重新输入有效的目录路径。")
        return

    with open("1.txt", "w") as file:
        create_directory_tree(directory, file)

    print("目录树已保存到1.txt文件中。")

if __name__ == "__main__":
    main()
