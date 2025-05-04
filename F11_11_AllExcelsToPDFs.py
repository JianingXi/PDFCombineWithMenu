import os
import win32com.client
from F11_LongWidthExcelToPDF import long_width_excel_to_pdf


def batch_convert_excels_to_pdfs(
    excel_folder: str,
    pdf_folder: str
):
    """
    批量将 excel_folder 里的 .xlsx 文件，调用 long_width_excel_to_pdf 转为 PDF，
    并保存到 pdf_folder 中，文件名保持一致，仅后缀改为 .pdf。
    """
    os.makedirs(pdf_folder, exist_ok=True)

    for fname in sorted(os.listdir(excel_folder)):
        if not fname.lower().endswith('.xlsx'):
            continue

        excel_path = os.path.join(excel_folder, fname)
        pdf_name   = os.path.splitext(fname)[0] + ".pdf"
        pdf_path   = os.path.join(pdf_folder, pdf_name)

        try:
            long_width_excel_to_pdf(excel_path, pdf_path)
            print(f"✅ 转换成功：{excel_path} → {pdf_path}")
        except Exception as e:
            print(f"❌ 转换失败：{excel_path}，错误：{e}")

if __name__ == "__main__":
    src_excels = r"C:\Users\xijia\Downloads\拆分单表_excels_new"
    dst_pdfs   = r"C:\Users\xijia\Downloads\拆分单表_pdf"

    batch_convert_excels_to_pdfs(src_excels, dst_pdfs)
