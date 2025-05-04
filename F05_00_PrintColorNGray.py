import os
from PIL import Image
import numpy as np

def process_image(image_path):
    # 定义灰度判断阈值
    GRAY_THRESHOLD = 10
    try:
        image = Image.open(image_path).convert('RGB')
        pixels = np.array(image).reshape(-1, 3).astype(int)  # 防止溢出

        # 向量化判断灰度
        diff_rg = np.abs(pixels[:, 0] - pixels[:, 1])
        diff_gb = np.abs(pixels[:, 1] - pixels[:, 2])
        diff_br = np.abs(pixels[:, 2] - pixels[:, 0])
        is_gray = (diff_rg < GRAY_THRESHOLD) & (diff_gb < GRAY_THRESHOLD) & (diff_br < GRAY_THRESHOLD)

        gray_count = np.sum(is_gray)
        total_count = pixels.shape[0]
        gray_ratio = gray_count / total_count
        color_ratio = 1 - gray_ratio

        return gray_ratio, color_ratio
    except Exception as e:
        print(f"Failed to process {image_path}: {e}")
        return None, None


def print_color_page_number(F3_compr_folder, out_file_txt_path, page_shift):
    color_rate_file = os.path.join(F3_compr_folder, 'image_color_ratio.txt')
    IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']
    # 遍历所有图片并编号
    results = []
    index = 1
    for root, _, files in os.walk(F3_compr_folder):
        for file in sorted(files):
            if any(file.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                image_path = os.path.join(root, file)
                gray_ratio, color_ratio = process_image(image_path)
                if gray_ratio is not None:
                    relative_name = os.path.relpath(image_path, F3_compr_folder)
                    results.append(f"{index}\t{relative_name}\tGray: {gray_ratio:.2%}\tColor: {color_ratio:.2%}")
                    index += 1

    # 输出到 txt 文件
    with open(color_rate_file, 'w', encoding='utf-8') as f:
        f.write("No.\tImage File\tGray Ratio\tColor Ratio\n")
        f.write("\n".join(results))

    # 初始化列表
    qualified_indices = []

    with open(color_rate_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 跳过第一行表头
    for line in lines[1:]:
        parts = line.strip().split('\t')
        if len(parts) >= 4:
            try:
                index = int(parts[0])
                color_ratio_str = parts[3].replace('Color:', '').strip().replace('%', '')
                color_ratio = float(color_ratio_str)
                if color_ratio >= 5.0:
                    qualified_indices.append(index)
            except Exception as e:
                print(f"Error parsing line: {line} - {e}")

    # 转为 NumPy 数组并打印
    qualified_indices_array = np.array(qualified_indices)
    # print("满足彩色占比的序号如下：")
    # print(qualified_indices_array)

    # ----- 页码列表 ----- #
    qualified_indices_array = qualified_indices_array + page_shift

    # 先排序
    sorted_array = np.sort(qualified_indices_array)

    # 合并连续数字为区间
    ranges = []
    start = end = sorted_array[0]

    for num in sorted_array[1:]:
        if num == end + 1:
            end = num
        else:
            if start == end:
                ranges.append(f"{start}")
            else:
                ranges.append(f"{start}-{end}")
            start = end = num

    # 添加最后一个区间
    if start == end:
        ranges.append(f"{start}")
    else:
        ranges.append(f"{start}-{end}")

    # 保存为 txt 文件
    with open(out_file_txt_path, 'w', encoding='utf-8') as f:
        for r in ranges:
            f.write(r + '\n')


def f05_00_print_color_n_gray(F3_compr_folder, out_file_txt_path, page_shift):
    # 设置路径
    print_color_page_number(F3_compr_folder, out_file_txt_path, page_shift)

