import os
from PIL import Image, ImageOps
from pdf2image import convert_from_path
import warnings

# 临时增加 Pillow 的最大像素限制
Image.MAX_IMAGE_PIXELS = None
warnings.simplefilter('error', Image.DecompressionBombWarning)

def convert_image_to_jpg(image_path, output_path, is_rot):
    with Image.open(image_path) as img:
        # 如果启用旋转，且图像宽度大于高度，则旋转图像
        if is_rot and img.width > img.height:
            img = img.rotate(270, expand=True)
            print(f"Rotated image: {image_path}")
        rgb_img = img.convert('RGB')
        rgb_img.save(output_path, 'JPEG', quality=95, dpi=(100, 100))
        print(f"Image converted to JPG: {output_path}")

def convert_pdf_to_jpg(input_pdf_path, output_folder, is_rot, all_pages=False, dpi=150):
    poppler_path = r'C:\Tools\poppler-24.02.0\Library\bin'  # 确保这个路径指向 Poppler 的 bin 目录
    if all_pages:
        pages = convert_from_path(input_pdf_path, dpi=dpi, poppler_path=poppler_path)
        for page_number, page in enumerate(pages):
            output_jpg_path = os.path.join(output_folder, f"page_{str(page_number + 1).zfill(4)}.jpg")
            page.save(output_jpg_path, 'JPEG', quality=95, dpi=(100, 100))
            if is_rot:
                rotate_image_if_landscape(output_jpg_path, is_rot)
            print(f"PDF page {page_number + 1} converted to JPG: {output_jpg_path}")
    else:
        pages = convert_from_path(input_pdf_path, dpi=dpi, first_page=1, last_page=1, poppler_path=poppler_path)
        output_jpg_path = os.path.join(output_folder, "page_0001.jpg")
        pages[0].save(output_jpg_path, 'JPEG', quality=95, dpi=(100, 100))
        if is_rot:
            rotate_image_if_landscape(output_jpg_path, is_rot)
        print(f"First page of PDF converted to JPG: {output_jpg_path}")

def rotate_image_if_landscape(image_path, is_rot):
    with Image.open(image_path) as img:
        if img.width > img.height and is_rot:
            img = img.rotate(270, expand=True)
            img.save(image_path, 'JPEG', quality=95, dpi=(100, 100))
            print(f"Rotated image: {image_path}")

def resize_to_same_length(image, target_length, min_length=500):
    # 保持图像的宽高比例调整大小
    if max(image.width, image.height) > target_length and min(image.width, image.height) > min_length:
        if image.width > image.height:
            new_width = target_length
            new_height = int(target_length * image.height / image.width)
        else:
            new_height = target_length
            new_width = int(target_length * image.width / image.height)
        return image.resize((new_width, new_height), Image.LANCZOS)
    else:
        return image  # 如果图像尺寸小于最小长度，则不调整大小

def process_files(source_folder, output_folder, is_rot, all_pages=False):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历所有图片，获取宽、高的最小值（用于后续调整图片尺寸）
    min_length = float('inf')
    max_length = 2000  # 设置一个最大长度，确保不会过度缩小图片

    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(('.png', '.gif', '.bmp', '.tiff', '.jpeg', '.jpg')):
                with Image.open(file_path) as img:
                    min_length = min(min_length, img.width, img.height)

    min_length = max(min_length, max_length)  # 使用最大长度的图片作为基准

    # 遍历所有文件，处理图片和PDF文件
    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, source_folder)
            relative_folder = os.path.dirname(relative_path)
            output_relative_folder = os.path.join(output_folder, relative_folder)

            if not os.path.exists(output_relative_folder):
                os.makedirs(output_relative_folder)

            if file.lower().endswith(('.png', '.gif', '.bmp', '.tiff', '.jpeg', '.jpg')):
                output_jpg_path = os.path.join(output_relative_folder, os.path.splitext(file)[0] + '.jpg')
                with Image.open(file_path) as img:
                    img = resize_to_same_length(img, min_length)
                    img = img.convert('RGB')  # 转换为RGB模式
                    img.save(output_jpg_path, 'JPEG', quality=95, dpi=(300, 300))
                    if is_rot:
                        rotate_image_if_landscape(output_jpg_path, is_rot)
            elif file.lower().endswith('.pdf'):
                pdf_output_folder = os.path.join(output_relative_folder, os.path.splitext(file)[0])
                if not os.path.exists(pdf_output_folder):
                    os.makedirs(pdf_output_folder)
                convert_pdf_to_jpg(file_path, pdf_output_folder, is_rot, all_pages)

# 示例使用
source_folder = r'C:\Users\xijia\Desktop\DoingPlatform\D20250319_第一届“泛雅杯”全国高校智慧课程设计大赛\线性与非线性\E05_附件作证材料1\A01原始整理版'
destination_folder = r'C:\Users\xijia\Desktop\DoingPlatform\D20250319_第一届“泛雅杯”全国高校智慧课程设计大赛\线性与非线性\E05_附件作证材料1\A02图片整理版'

is_rot = 0  # 设置为非 0 则启用旋转功能，若设置为 0 则不启用
all_pages = True  # 设置为 True 以转换 PDF 的所有页面，否则 False 仅转换首页

process_files(source_folder, destination_folder, is_rot, all_pages)
