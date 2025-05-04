import os
from PIL import Image, ImageDraw, ImageFont
import warnings
import natsort

# 保持 Pillow 的最大像素限制
Image.MAX_IMAGE_PIXELS = None
warnings.simplefilter('error', Image.DecompressionBombWarning)


def convert_to_dpi(image, target_dpi):
    image.info['dpi'] = (target_dpi, target_dpi)
    return image


def resize_to_target_length(image, target_length):
    if image.width > image.height:
        new_width = target_length
        new_height = int(target_length * image.height / image.width)
    else:
        new_height = target_length
        new_width = int(target_length * image.width / image.height)
    return image.resize((new_width, new_height), Image.LANCZOS)


def add_border_and_pagenumber(image, page_number, target_length, border_size=30, border_color=(255, 255, 255),
                              font_size=20):
    img = resize_to_target_length(image, target_length)
    new_width = img.width + 2 * border_size
    new_height = img.height + 2 * border_size
    new_img = Image.new('RGB', (new_width, new_height), border_color)
    new_img.paste(img, (border_size, border_size))
    draw = ImageDraw.Draw(new_img)
    draw.rectangle([(border_size - 1, border_size - 1), (new_width - border_size, new_height - border_size)],
                   outline="black")
    try:
        font = ImageFont.truetype("arial.ttf", int(font_size * 0.75))
    except IOError:
        font = ImageFont.load_default()
    text = f"{page_number}"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (new_width - text_width) // 2
    text_y = new_height - text_height - border_size // 2
    draw.text((text_x, text_y), text, fill="black", font=font)
    return new_img


def process_images(input_folder, output_folder, initial_page_number=1, target_dpi=450, target_length=1920,
                   add_border_and_page_number=True):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_files = []
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith('.jpg'):
                image_files.append(os.path.join(root, file))

    image_files = natsort.natsorted(image_files)

    for i, image_path in enumerate(image_files):
        with Image.open(image_path) as img:
            img = img.convert('RGB')
            output_filename = f"{str(i + initial_page_number).zfill(4)}_{os.path.relpath(image_path, input_folder).replace(os.sep, '_')}"
            output_path = os.path.join(output_folder, output_filename)

            if add_border_and_page_number:
                processed_img = add_border_and_pagenumber(img, i + initial_page_number, target_length)
            else:
                processed_img = resize_to_target_length(img, target_length)

            processed_img.save(output_path, 'JPEG', quality=100, dpi=(target_dpi, target_dpi))
            print(f"Processed {image_path}")


def f02_add_pag_number(input_folder, output_folder, initial_page_number, target_dpi, target_length,
                       add_border_and_page_number):
    """
    initial_page_number = 1  # 设置初始页码
    target_dpi = 800
    target_length = 1920
    add_border_and_page_number = True
    """
    process_images(input_folder, output_folder, initial_page_number, target_dpi, target_length,
                   add_border_and_page_number)
