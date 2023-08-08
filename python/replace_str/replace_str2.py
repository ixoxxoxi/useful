import re
import os

# 提示用户输入文件路径
file_path = input("请输入js文件路径：")

# 检查文件是否存在
if not os.path.isfile(file_path):
    print("文件不存在！")
    exit()

# 检查文件写入权限
if not os.access(file_path, os.W_OK):
    print("没有文件写入权限！")
    exit()

# 读取文件内容，指定编码为UTF-8
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# 使用正则表达式匹配键值对
pattern = r"(\w+)\s*:\s*'([^']*)'"
matches = re.findall(pattern, content, re.DOTALL)

# 替换匹配到的字符串
for match in matches:
    key = match[0]
    value = match[1]
    if '{' in value:
        new_value = value.replace('{', "{'{").replace('}', "}'}")
        content = re.sub(fr"{key}\s*:\s*'({re.escape(value)})'", f"{key}: \"{new_value}\"", content)

# 将修改后的内容写回文件
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(content)

print("处理完成！")
