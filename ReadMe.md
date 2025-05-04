# PDF and Image Processing Scripts

## Overview

This project provides a set of Python scripts for processing PDFs and images, including converting PDFs to images, adding page numbers to images, merging images into a single PDF, and creating an index document in DOCX format.

本项目提供了一组用于处理PDF和图像的Python脚本，包括将PDF转换为图像、在图像上添加页码、将图像合并为单个PDF，以及创建DOCX格式的索引文档。

## Features

- **Convert PDF to Images**: Convert each page of a PDF to an image.
- **Add Page Numbers**: Add page numbers and borders to images.
- **Merge Images to PDF**: Merge multiple images into a single PDF document.
- **Create Index Document**: Generate a DOCX document with an index of all images.

功能特点：

- **将PDF转换为图像**：将PDF的每一页转换为图像。
- **添加页码**：在图像上添加页码和边框。
- **将图像合并为PDF**：将多张图像合并为一个PDF文档。
- **创建索引文档**：生成包含所有图像索引的DOCX文档。

## Requirements

- Python 3.x
- PIL (Pillow)
- pdf2image
- fpdf
- python-docx

安装要求：

- Python 3.x
- PIL (Pillow)
- pdf2image
- fpdf
- python-docx

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/PDFImageProcessing.git
   cd PDFImageProcessing
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

安装步骤：

1. 克隆仓库：

   ```bash
   git clone https://github.com/yourusername/PDFImageProcessing.git
   cd PDFImageProcessing
   ```

2. 安装所需的软件包：

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Convert PDF to Images

To convert a PDF to images, use the `F01TraverseAllPDFImageToImage.py` script. Make sure to specify the source folder containing the PDFs and the destination folder for the images.

```bash
python F01_00_TraverseAllPDFImageToImage.py /path/to/source_folder /path/to/destination_folder
```

### Add Page Numbers to Images

To add page numbers and borders to images, use the `F02AddPageNumber.py` script. Specify the input folder containing the images and the output folder for the processed images.

```bash
python F02_00_AddPageNumber.py /path/to/input_folder /path/to/output_folder
```

### Merge Images to Single PDF

To merge multiple images into a single PDF document, use the `F03MergeImgToSinglePDF.py` script. Specify the folder containing the images and the output PDF file path.

```bash
python F03_00_MergeImgToSinglePDF.py /path/to/image_folder /path/to/output.pdf
```

### Create Index Document

To generate a DOCX document with an index of all images, use the `F04CreateMenuDocx.py` script. Specify the input folder containing the images and the output folder for the DOCX file.

```bash
python F04_00_CreateMenuDocx.py /path/to/input_folder /path/to/output_folder
```

使用方法：

### 将PDF转换为图像

要将PDF转换为图像，请使用 `F01TraverseAllPDFImageToImage.py` 脚本。请确保指定包含PDF的源文件夹和用于保存图像的目标文件夹。

```bash
python F01_00_TraverseAllPDFImageToImage.py /path/to/source_folder /path/to/destination_folder
```

### 在图像上添加页码

要在图像上添加页码和边框，请使用 `F02AddPageNumber.py` 脚本。指定包含图像的输入文件夹和保存处理后图像的输出文件夹。

```bash
python F02_00_AddPageNumber.py /path/to/input_folder /path/to/output_folder
```

### 将图像合并为单个PDF

要将多张图像合并为一个PDF文档，请使用 `F03MergeImgToSinglePDF.py` 脚本。指定包含图像的文件夹和输出PDF文件路径。

```bash
python F03_00_MergeImgToSinglePDF.py /path/to/image_folder /path/to/output.pdf
```

### 创建索引文档

要生成包含所有图像索引的DOCX文档，请使用 `F04CreateMenuDocx.py` 脚本。指定包含图像的输入文件夹和用于保存DOCX文件的输出文件夹。

```bash
python F04_00_CreateMenuDocx.py /path/to/input_folder /path/to/output_folder
```

## Script Details

### F01TraverseAllPDFImageToImage.py

This script converts PDF files to images. It can process all pages of a PDF or just the first page.

- **Input**: Source folder containing PDF files.
- **Output**: Destination folder with converted images.

### F02AddPageNumber.py

This script adds page numbers and borders to images.

- **Input**: Folder containing images.
- **Output**: Folder with images that have added page numbers and borders.

### F03MergeImgToSinglePDF.py

This script merges multiple images into a single PDF document.

- **Input**: Folder containing images.
- **Output**: Single PDF file.

### F04CreateMenuDocx.py

This script generates a DOCX document with an index of all images in a specified folder.

- **Input**: Folder containing images.
- **Output**: DOCX file with the index.

脚本详情：

### F01TraverseAllPDFImageToImage.py

此脚本将PDF文件转换为图像。它可以处理PDF的所有页面或仅处理首页。

- **输入**：包含PDF文件的源文件夹。
- **输出**：包含转换后图像的目标文件夹。

### F02AddPageNumber.py

此脚本在图像上添加页码和边框。

- **输入**：包含图像的文件夹。
- **输出**：添加了页码和边框的图像文件夹。

### F03MergeImgToSinglePDF.py

此脚本将多张图像合并为一个PDF文档。

- **输入**：包含图像的文件夹。
- **输出**：单个PDF文件。

### F04CreateMenuDocx.py

此脚本生成包含指定文件夹中所有图像索引的DOCX文档。

- **输入**：包含图像的文件夹。
- **输出**：包含索引的DOCX文件。


## Detailed Steps for Each Script

### F01TraverseAllPDFImageToImage.py

#### Step 1: Load PDF Files

The script loads PDF files from the specified source folder.

#### Step 2: Convert PDF Pages to Images

It converts each page of the PDF files to JPG images. If `all_pages` is set to True, all pages are converted; otherwise, only the first page is converted.

#### Step 3: Rotate Images if Necessary

The script checks if the images need to be rotated (for landscape orientation) and rotates them accordingly.

#### Step 4: Save the Images

The converted images are saved to the specified destination folder.

### F02AddPageNumber.py

#### Step 1: Load Images

The script loads images from the specified input folder.

#### Step 2: Resize Images

It resizes images to a target length while maintaining the aspect ratio.

#### Step 3: Add Borders and Page Numbers

The script adds borders and page numbers to the images.

#### Step 4: Save the Processed Images

The processed images are saved to the specified output folder.

### F03MergeImgToSinglePDF.py

#### Step 1: Load Images

The script loads JPG images from the specified input folder.

#### Step 2: Create PDF Pages

It creates a new PDF document and adds each image as a page, ensuring proper orientation and scaling.

#### Step 3: Save the PDF

The resulting PDF is saved to the specified output path.

### F04CreateMenuDocx.py

#### Step 1: Load Images

The script loads JPG images from the specified input folder.

#### Step 2: Create DOCX Document

It creates a DOCX document and adds each image file name with corresponding page numbers.

#### Step 3: Save the DOCX

The DOCX document is saved to the specified output folder.

## Examples

Here are some examples of how to use the scripts.

### Example 1: Convert PDF to Images

```python
from F01_00_TraverseAllPDFImageToImage import process_files

source_folder = '/path/to/source_folder'
destination_folder = '/path/to/destination_folder'
all_pages = True

process_files(source_folder, destination_folder, all_pages)
```

### Example 2: Add Page Numbers to Images

```python
from F02_00_AddPageNumber import process_images

input_folder = '/path/to/input_folder'
output_folder = '/path/to/output_folder'
target_dpi = 300
target_length = 1920
add_border_and_page_number = True

process_images(input_folder, output_folder, target_dpi, target_length, add_border_and_page_number)
```

### Example 3: Merge Images to Single PDF

```python
from F03_00_MergeImgToSinglePDF import images_to_pdf

image_folder = '/path/to/image_folder'
output_pdf_path = '/path/to/output.pdf'

images_to_pdf(image_folder, output_pdf_path)
```

### Example 4: Create Index Document

```python
from F04_00_CreateMenuDocx import generate_index

input_folder = '/path/to/input_folder'
output_folder = '/path/to/output_folder'

generate_index(input_folder, output_folder)
```

示例：

### 示例1：将PDF转换为图像

```python
from F01_00_TraverseAllPDFImageToImage import process_files

source_folder = '/path/to/source_folder'
destination_folder = '/path/to/destination_folder'
all_pages = True

process_files(source_folder, destination_folder, all_pages)
```

### 示例2：在图像上添加页码

```python
from F02_00_AddPageNumber import process_images

input_folder = '/path/to/input_folder'
output_folder = '/path/to/output_folder'
target_dpi = 300
target_length = 1920
add_border_and_page_number = True

process_images(input_folder, output_folder, target_dpi, target_length, add_border_and_page_number)
```

### 示例3：将图像合并为单个PDF

```python
from F03_00_MergeImgToSinglePDF import images_to_pdf

image_folder = '/path/to/image_folder'
output_pdf_path = '/path/to/output.pdf'

images_to_pdf(image_folder, output_pdf_path)
```

### 示例4：创建索引文档

```python
from F04_00_CreateMenuDocx import generate_index

input_folder = '/path/to/input_folder'
output_folder = '/path/to/output_folder'

generate_index(input_folder, output_folder)
```

## Troubleshooting

### Issue: Incorrect Page Order

Ensure that the image files are named sequentially and follow the correct order before processing.

### Issue: Missing Images

Verify that all images are present in the specified directories and are named correctly. Check the console output for any error messages.

### Issue: Unsupported File Format

Ensure that all files in the specified directories are in the correct format (PDF for conversion, JPG for merging).

故障排除：

### 问题：页面顺序错误

确保图像文件按顺序命名，并在处理前遵循正确的顺序。

### 问题：缺少图像

验证所有图像是否存在于指定目录中，并正确命名。检查控制台输出以获取任何错误消息。

### 问题：不支持的文件格式

确保指定目录中的所有文件都为正确的格式（转换时为PDF，合并时为JPG）。

## Future Improvements

Here are some potential improvements for the project:

- **Enhanced Error Handling**: Improve error handling to provide more informative messages and handle edge cases.
- **Additional File Formats**: Add support for additional file formats like PNG, TIFF.
- **Automatic Sorting**: Implement automatic sorting of image files to ensure correct order.
- **GUI Interface**: Develop a graphical user interface for easier use.

未来改进：

以下是该项目的一些潜在改进：

- **增强错误处理**：改进错误处理以提供更有用的信息并处理边缘情况。
- **更多文件格式**：添加对其他文件格式（如PNG，TIFF）的支持。
- **自动排序**：实现图像文件的自动排序，确保正确的顺序。
- **图形用户界面**：开发图形用户界面以便更容易使用。

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue if you encounter any problems.

欢迎贡献！如果你遇到任何问题，请随时提交拉取请求或打开问题。

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

许可证：

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。

