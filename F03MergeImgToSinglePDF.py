import os
from PIL import Image
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        pass

def compress_image(image_path, output_path, quality):
    img = Image.open(image_path)
    img = img.convert('RGB')
    img.save(output_path, 'JPEG', quality=quality)
    return output_path

def images_to_pdf(input_folder, output_pdf_path, compressed_folder, quality):
    # 创建压缩后的图片存储文件夹
    if not os.path.exists(compressed_folder):
        os.makedirs(compressed_folder)

    # 获取所有JPG文件，按字母表顺序排序
    image_files = sorted([f for f in os.listdir(input_folder) if f.lower().endswith('.jpg')])

    if not image_files:
        print("No .jpg files found in the specified folder.")
        return

    pdf = PDF()
    pdf.set_auto_page_break(0)

    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        compressed_image_path = os.path.join(compressed_folder, image_file)

        # 压缩图像
        compress_image(image_path, compressed_image_path, quality)

        img = Image.open(compressed_image_path)
        width, height = img.size

        # 将图像尺寸转换为PDF尺寸（单位为毫米，1像素 = 0.264583毫米）
        width_mm, height_mm = width * 0.264583, height * 0.264583

        # 设置页面尺寸
        pdf.add_page(orientation='P' if height_mm > width_mm else 'L')

        # 获取页面宽度和高度
        page_width_mm = pdf.w
        page_height_mm = pdf.h

        # 计算缩放比例
        scale = min(page_width_mm / width_mm, page_height_mm / height_mm)

        # 计算图像在页面上的显示尺寸
        display_width_mm = width_mm * scale
        display_height_mm = height_mm * scale

        # 计算图像在页面上的居中位置
        x = (page_width_mm - display_width_mm) / 2
        y = (page_height_mm - display_height_mm) / 2

        # 添加图像
        pdf.image(compressed_image_path, x, y, display_width_mm, display_height_mm)

    # 确保输出路径是一个有效的文件路径
    if not output_pdf_path.lower().endswith('.pdf'):
        output_pdf_path = os.path.join(output_pdf_path, 'output.pdf')

    pdf.output(output_pdf_path, "F")
    print(f"PDF file created: {output_pdf_path}")

# 示例使用
input_folder = r'C:\Users\素材Temp\'
compressed_folder = r'C:\Users\Compress'
output_pdf_path = r'C:\Users\\统计.pdf'

quality = 95  # 设置压缩率，范围在1（最差）到95（最好）之间

images_to_pdf(input_folder, output_pdf_path, compressed_folder, quality)
