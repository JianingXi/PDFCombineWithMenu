import os
import pandas as pd
import re
import shutil

import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_pdf import PdfPages
import shutil

import fitz  # PyMuPDF
from fpdf import FPDF

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimSun']
matplotlib.rcParams['axes.unicode_minus'] = False


# ----- Excel Split into Sheets ----- #
def split_sheets_to_excels(
        input_excel_path: str,
        output_dir: str,
        file_name_prefix: str = None
):
    """
    将一个多 sheet 的 Excel，拆分成多个单 sheet 的 Excel 文件，
    且不新增任何表头行（完全保留原有内容）。

    参数
    ----
    input_excel_path : str
        原始 Excel 文件路径（可以有多个 sheet）。
    output_dir : str
        拆分后文件输出目录；不存在时会自动创建。
    file_name_prefix : str 或 None
        拆分后文件名前缀，如果为 None，则使用原文件名加 sheet 名称。
    """
    os.makedirs(output_dir, exist_ok=True)

    # 1) 以 header=None 读取，所有行全部作为数据
    sheets_dict = pd.read_excel(
        input_excel_path,
        sheet_name=None,  # 读取所有 sheet
        header=None,  # 不把任何行当作表头
        dtype=str
    )

    base_name = (
        os.path.splitext(os.path.basename(input_excel_path))[0]
        if file_name_prefix is None
        else file_name_prefix
    )

    # 2) 逐个 sheet 写出，不输出额外的 header 或 index
    for sheet_name, df in sheets_dict.items():
        safe_name = "".join(c if c.isalnum() or c in (" ", "_", "-") else "_" for c in sheet_name)
        out_file = os.path.join(output_dir, f"{base_name}_{safe_name}.xlsx")

        # header=False：不写列名； index=False：不写行号
        df.to_excel(out_file, index=False, header=False)
        print(f"✅ 已拆分 sheet '{sheet_name}' → {out_file}")


# ----- Body and Head Recognition ----- #
def detect_header_rows_by_name_id(df: pd.DataFrame, max_scan_rows: int = 20) -> int:
    """
    方法一：通过“姓名在第 0 列、学号在第 1 列”这一模式，定位首个数据行。
    返回值 i 表示前 i 行都是表头；如果未找到则返回 0。
    """
    id_pattern = re.compile(r'^\d{6,12}$')  # 学号：6–12 位数字
    name_pattern = re.compile(r'[\u4e00-\u9fff].*[\u4e00-\u9fff]')  # 至少两个汉字

    scan_n = min(len(df), max_scan_rows)
    for i in range(scan_n):
        row = df.iloc[i].astype(str).fillna("")
        if name_pattern.search(row.iloc[0].strip()) and id_pattern.fullmatch(row.iloc[1].strip()):
            return i
    return 0


def detect_header_rows_by_datapattern(df: pd.DataFrame,
                                      max_scan_rows: int = 20,
                                      data_threshold: float = 0.5) -> int:
    """
    方法二：通过“数字/日期特征突变”来定位数据区起点，把它之前的行当表头。
    返回值 i 表示第 i 行首个满足 data_ratio >= data_threshold 的行为数据行。
    """
    date_or_num = re.compile(r'\d')
    scan_n = min(len(df), max_scan_rows)

    for i in range(scan_n):
        row = df.iloc[i].astype(str).fillna("")
        data_cells = sum(bool(date_or_num.search(cell)) for cell in row)
        if data_cells / len(row) >= data_threshold:
            return i
    return scan_n


def detect_header_rows(df: pd.DataFrame) -> int:
    """
    先尝试方法一（姓名+学号）；若失败，再降级用方法二（数字/日期突变）。
    确保至少返回 1。
    """
    hdr = detect_header_rows_by_name_id(df)
    if hdr > 0:
        return hdr
    hdr2 = detect_header_rows_by_datapattern(df)
    return max(1, hdr2)


def extract_and_pickle(folder_path: str, output_folder: str):
    """
    遍历目录下所有 .xls/.xlsx 文件及其所有 sheet，
    自动识别表头行数，并将表头和正文分别存为两个 pickle 文件。

    输出文件命名示例：
      {原文件名}_{sheet_name}_header.pkl
      {原_file_name}_{sheet_name}_body.pkl
    """
    os.makedirs(output_folder, exist_ok=True)

    for fname in sorted(os.listdir(folder_path)):
        if not fname.lower().endswith(('.xls', '.xlsx')):
            continue

        base_name = os.path.splitext(fname)[0]
        full_path = os.path.join(folder_path, fname)
        sheets = pd.read_excel(full_path, sheet_name=None, header=None, dtype=str)

        for sheet_name, df in sheets.items():
            header_count = detect_header_rows(df)

            # 分割表头和正文
            header_df = df.iloc[:header_count].reset_index(drop=True)
            body_df = df.iloc[header_count:].reset_index(drop=True)

            # 构造保存路径
            safe_sheet = "".join(c if c.isalnum() or c in (" ", "_") else "_" for c in sheet_name)
            header_pkl = os.path.join(output_folder, f"{base_name}_{safe_sheet}_header.pkl")
            body_pkl = os.path.join(output_folder, f"{base_name}_{safe_sheet}_body.pkl")

            # 存为 pickle
            header_df.to_pickle(header_pkl)
            body_df.to_pickle(body_pkl)



            print(f"✅ {fname} [{sheet_name}]: header → {header_pkl}, body → {body_pkl}")
    row_count = body_df.shape[0]
    return row_count


# ----- Body Split with Heads ----- #
def best_max_rows(num_row):  # 凑数字，找到最佳max_rows，用于拆分学生
    candidates = [(r, (r - num_row % r) % r) for r in range(30, 42)]
    best = min(candidates, key=lambda x: x[1])  # 按delta排序
    return best[0]  # 返回 max_rows

def split_body_and_export_excels(pkl_folder: str, output_folder: str, max_rows: int = 35):
    """
    对 pkl_folder 中成对的 header.pkl 和 body.pkl 文件进行处理：
    - 读取 header_df 和 body_df
    - 如果 body_df 行数 > max_rows，则分块（每块不超过 max_rows 行）
    - 每个块与 header_df 合并后输出为一个单独的 Excel 文件

    输出文件命名格式：
      {base_name}_{sheet_name}_part{n}.xlsx
    """
    os.makedirs(output_folder, exist_ok=True)

    # 遍历所有 header.pkl 文件
    for fname in sorted(os.listdir(pkl_folder)):
        if not fname.endswith("_header.pkl"):
            continue

        base = fname[:-11]  # 去掉 "_header.pkl"
        header_path = os.path.join(pkl_folder, fname)
        body_path = os.path.join(pkl_folder, f"{base}_body.pkl")

        # 如果没有对应的 body.pkl，跳过
        if not os.path.exists(body_path):
            print(f"⚠️ 找不到对应的 body 文件：{body_path}, 跳过")
            continue

        # 读取 DataFrame
        header_df = pd.read_pickle(header_path)
        body_df = pd.read_pickle(body_path)

        # 计算需要多少块
        total_rows = len(body_df)
        num_parts = (total_rows + max_rows - 1) // max_rows or 1

        for part in range(num_parts):
            start = part * max_rows
            end = start + max_rows
            chunk = body_df.iloc[start:end].reset_index(drop=True)

            # 合并 header + chunk
            out_df = pd.concat([header_df, chunk], ignore_index=True)

            # 构造输出文件名
            safe_base = "".join(c if c.isalnum() or c in (" ", "_") else "_" for c in base)
            out_fname = f"{safe_base}_part{part + 1}.xlsx"
            out_path = os.path.join(output_folder, out_fname)

            # 导出 Excel，不写索引
            out_df.to_excel(out_path, index=False, header=False)
            print(f"✅ 已输出：{out_path} （包含 {len(chunk)} 行数据）")


# ----- Temp file Deletion ----- #

def delete_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"✅ 已删除文件夹及其内容：{folder_path}")
    else:
        print(f"⚠️ 文件夹不存在：{folder_path}")


# ----- Excel to TSVs ----- #
def excel_to_tsv(src_excels, dst_tsv):
    os.makedirs(dst_tsv, exist_ok=True)

    for fname in os.listdir(src_excels):
        if not fname.lower().endswith(('.xls', '.xlsx')):
            continue
        file_path = os.path.join(src_excels, fname)
        xls = pd.ExcelFile(file_path)

        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name, dtype=str)
            tsv_name = f"{os.path.splitext(fname)[0]}_{sheet_name}.tsv"
            tsv_path = os.path.join(dst_tsv, tsv_name)
            df.to_csv(tsv_path, sep='\t', index=False)
            print(f"✅ 已保存：{tsv_path}")


# ----- TSVs to PDFs ----- #

# 拆分列函数
def split_columns(df, max_total_width=110):
    """
    将列名按字符长度大致均分为若干组，使每页总宽度尽量接近 max_total_width 且不至于最后一页太少。
    """
    import numpy as np

    # 估算每列宽度：列名长度 + 平均单元格长度
    est_widths = []
    for col in df.columns:
        col_strs = df[col].astype(str)
        avg_len = col_strs.map(len).mean()
        est_width = len(str(col)) + avg_len
        est_widths.append(est_width)

    # 累加并计算总宽度
    total_width = sum(est_widths)
    est_num_pages = max(1, round(total_width / max_total_width))

    # 使用累加法按宽度均分
    indices = np.arange(len(df.columns))
    sorted_idx = sorted(indices, key=lambda i: -est_widths[i])  # 按宽度从大到小
    pages = [[] for _ in range(est_num_pages)]
    page_widths = [0] * est_num_pages

    for i in sorted_idx:
        # 放入当前最“瘦”的页
        target = page_widths.index(min(page_widths))
        pages[target].append(df.columns[i])
        page_widths[target] += est_widths[i]

    # 按原始列顺序排序每页
    groups = [sorted(page, key=lambda c: df.columns.get_loc(c)) for page in pages]
    return groups



def tsv_to_pdf(src_tsv_dir, output_pdf_dir):
    os.makedirs(output_pdf_dir, exist_ok=True)
    # 主循环
    for fname in sorted(os.listdir(src_tsv_dir)):
        if not fname.endswith(".tsv"):
            continue

        fpath = os.path.join(src_tsv_dir, fname)
        df_raw = pd.read_csv(fpath, sep='\t', header=None, dtype=str).fillna("")

        if len(df_raw) < 2:
            print(f"⚠️ 文件过短，跳过：{fname}")
            continue

        # 标题和副标题
        base_name = os.path.splitext(fname)[0]
        title_clean = re.sub(r'(_Sheet\d+_part\d+_Sheet\d+)$', '', base_name)
        subtitle_raw = "  ".join(df_raw.iloc[1].astype(str))
        subtitle_clean = re.sub(r'[\r\n]+', ' ', subtitle_raw).strip()

        # 设置表头和正文
        df_raw.columns = df_raw.iloc[0]
        df_data = df_raw.iloc[2:].reset_index(drop=True)

        groups = split_columns(df_data, max_total_width=110)
        pdf_path = os.path.join(output_pdf_dir, f"{base_name}.pdf")

        with PdfPages(pdf_path) as pdf:
            for i, cols in enumerate(groups):
                sub_df = df_data[cols]

                fig, ax = plt.subplots(figsize=(11.69, 8.27))  # A4横向
                fig.subplots_adjust(top=0.88, bottom=0.05, left=0.05, right=0.95)
                ax.axis('off')

                # 标题、副标题（居中）
                fig.text(0.5, 0.95, title_clean, fontsize=8, ha='center', va='top')
                if subtitle_clean:
                    fig.text(0.5, 0.91, subtitle_clean, fontsize=6, ha='center', va='top')

                # 表格
                tbl = ax.table(cellText=sub_df.values,
                               colLabels=sub_df.columns,
                               cellLoc='center',
                               loc='center')

                tbl.auto_set_font_size(False)
                tbl.set_fontsize(6)
                tbl.scale(1.0, 0.9)

                for key, cell in tbl.get_celld().items():
                    cell.set_linewidth(0.5)

                pdf.savefig(fig, bbox_inches='tight', dpi=300)
                plt.close(fig)

        print(f"✅ 已生成 PDF：{pdf_path}")


# ----- PDF Merge ----- #

# 分组函数：去掉 _SheetX_partX_SheetX.pdf 尾巴
def get_group_key(filename):
    return re.sub(r'_Sheet\d+_part\d+_Sheet\d+\.pdf$', '', filename)


def pdf_merge(src_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    # 分组文件
    groups = {}
    for fname in sorted(os.listdir(src_dir)):
        if not fname.lower().endswith(".pdf"):
            continue
        key = get_group_key(fname)
        groups.setdefault(key, []).append(fname)

    # 合并每组
    for group_name, files in groups.items():
        pdf = FPDF(orientation='L', unit='mm', format='A4')  # 横向 A4
        page_count = 0

        for file in files:
            pdf_path = os.path.join(src_dir, file)
            try:
                doc = fitz.open(pdf_path)
                for idx, page in enumerate(doc):
                    pix = page.get_pixmap(dpi=150)
                    temp_img = f"__temp_{group_name}_{page_count}.png"
                    pix.save(temp_img)

                    # 添加新页
                    pdf.add_page()
                    pdf.image(temp_img, x=5, y=5, w=287)  # 留白 5mm
                    os.remove(temp_img)
                    page_count += 1
                doc.close()
            except Exception as e:
                print(f"❌ 转换失败：{file}\n错误：{e}")
                continue

        merged_path = os.path.join(output_dir, f"{group_name}_merged.pdf")
        pdf.output(merged_path)
        print(f"✅ 已合并输出：{merged_path}")


# ----- PDF with page numbers ----- #
def add_page_numbers_to_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    for page_number in range(len(doc)):
        page = doc[page_number]
        text = str(page_number + 1)
        font_size = 6

        width = page.rect.width
        height = page.rect.height
        text_width = fitz.get_text_length(text, fontname="Times-Roman", fontsize=font_size)

        x = (width - text_width) / 2
        y = height - 10  # 更靠底部

        page.insert_text(
            (x, y),
            text,
            fontname="Times-Roman",
            fontsize=font_size,
            color=(0, 0, 0),
        )

    doc.save(pdf_path, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
    doc.close()
    print(f"✅ 添加页码完成：{os.path.basename(pdf_path)}")


def pdf_with_page_numbers(output_dir):
    # 批量处理
    for fname in os.listdir(output_dir):
        if fname.lower().endswith(".pdf"):
            full_path = os.path.join(output_dir, fname)
            add_page_numbers_to_pdf(full_path)


def pdf_rename_remove_merged(pdf_dir: str):
    for fname in os.listdir(pdf_dir):
        if fname.lower().endswith("_merged.pdf"):
            old_path = os.path.join(pdf_dir, fname)
            new_name = fname.replace("_merged", "")
            new_path = os.path.join(pdf_dir, new_name)
            os.rename(old_path, new_path)
            print(f"✅ 重命名：{fname} ➜ {new_name}")


# ----- Main ----- #
def excels_to_splited_pdfs_for_chaoxing(base_dir: str, excel_file_name: str):
    src_excel = os.path.join(base_dir, excel_file_name)
    src_folder = os.path.join(base_dir, '拆分单表_raw')
    pkl_dir = os.path.join(base_dir, '拆分单表_pkl')
    excel_dir = os.path.join(base_dir, '拆分单表_excels')
    src_tsv = os.path.join(base_dir, '拆分单表_tsv')
    src_pdf = os.path.join(base_dir, '拆分单表_pdf')
    output_dir = os.path.join(base_dir, 'Printed_DPFs')

    # ----- excels_sheet_head_body_spliter ----- #
    split_sheets_to_excels(src_excel, src_folder)
    num_row = extract_and_pickle(src_folder, pkl_dir)
    split_body_and_export_excels(pkl_dir, excel_dir, max_rows=best_max_rows(num_row))

    delete_folder(src_folder)
    delete_folder(pkl_dir)

    # ----- excels_to_pdfs ----- #
    excel_to_tsv(excel_dir, src_tsv)
    tsv_to_pdf(src_tsv, src_pdf)

    pdf_merge(src_pdf, output_dir)

    pdf_with_page_numbers(output_dir)
    pdf_rename_remove_merged(output_dir)

    delete_folder(excel_dir)
    delete_folder(src_tsv)
    delete_folder(src_pdf)
