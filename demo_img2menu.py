import os
from F01_00_TraverseAllPDFImageToImage import f01_traverse_all_pdf_image_to_image
from F01_01_FrontPageDirRename import rename_and_move_files
from F02_00_AddPageNumber import f02_add_pag_number
from F03_00_MergeImgToSinglePDF import f03_merge_img_to_single_pdf
from F04_00_CreateMenuDocx import f04_create_menu_docx
from F05_00_PrintColorNGray import f05_00_print_color_n_gray

base_dir = r'C\abc'
source_folder = os.path.join(base_dir, '材料')
F1_img_folder = os.path.join(base_dir, '材料_1图片版')
F2_num_folder = os.path.join(base_dir, '材料_2页码版')
F3_compr_folder = os.path.join(base_dir, '材料_3压缩版')

F4_num_pdf = os.path.join(base_dir, '材料_02内容.pdf')
F5_menu_docx = os.path.join(base_dir, '材料_01目录.docx')



is_rot = 1  # 设置为非 0 则启用旋转功能，若设置为 0 则不启用
all_pages = True  # 设置为 True 以转换 PDF 的所有页面，否则 False 仅转换首页

f01_traverse_all_pdf_image_to_image(source_folder, F1_img_folder, is_rot, all_pages)



rename_and_move_files(F1_img_folder)



initial_page_number = 1  # 设置初始页码
target_dpi = 800
target_length = 1920
add_border_and_page_number = True

f02_add_pag_number(F1_img_folder, F2_num_folder, initial_page_number, target_dpi, target_length,
                   add_border_and_page_number)

quality = 95  # 设置压缩率，范围在1（最差）到95（最好）之间

f03_merge_img_to_single_pdf(F2_num_folder, F4_num_pdf, F3_compr_folder, quality)

initial_page_number = 1  # 替换为你的初始页码

f04_create_menu_docx(F3_compr_folder, F5_menu_docx, initial_page_number)



out_file_txt_path = os.path.join(base_dir, '材料_打印为彩色的页码.txt')

page_shift = 2  # 目录的页数
f05_00_print_color_n_gray(F3_compr_folder, out_file_txt_path, page_shift)