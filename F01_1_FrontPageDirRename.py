import os
import shutil


def rename_and_move_files(directory):
    # 遍历指定目录下的所有文件夹
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)

            # 获取文件夹中的所有文件
            files_in_dir = os.listdir(dir_path)

            # 如果文件夹中只有一个文件
            if len(files_in_dir) == 1:
                file_name = files_in_dir[0]
                file_path = os.path.join(dir_path, file_name)

                # 获取文件的扩展名
                file_extension = os.path.splitext(file_name)[1]

                # 新的文件名（使用文件夹的名字）
                new_file_name = f"{dir_name}{file_extension}"
                new_file_path = os.path.join(root, new_file_name)

                # 重命名并移动文件
                shutil.move(file_path, new_file_path)

                # 删除空的文件夹
                os.rmdir(dir_path)
                print(
                    f"Moved and renamed '{file_name}' to '{new_file_name}' and deleted the empty folder '{dir_name}'.")


# 使用示例
directory_to_check = r"C:\Users\xijia\Desktop\DoingPlatform\D20250308_广州市青年人才托举\B02附件\5-奖励荣誉证书、著作封面、文章首页、专利证书等\3论文首页"  # 替换为你要检查的目录路径
rename_and_move_files(directory_to_check)