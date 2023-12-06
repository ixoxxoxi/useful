import os
import pyvips

def convert_tgs_to_gif(folder_path, save_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.tgs'):
            tgs_path = os.path.join(folder_path, file_name)
            gif_path = os.path.join(save_path, file_name.replace('.tgs', '.gif'))
            
            image = pyvips.Image.new_from_file(tgs_path)
            image.write_to_file(gif_path, option='gif')
            
            print(f"Converted {tgs_path} to {gif_path}")

# 指定文件夹路径
folder_path = '指定文件夹路径'

# 提示用户输入保存路径
save_path = input("请输入保存路径：")

# 调用函数进行转换
convert_tgs_to_gif(folder_path, save_path)
