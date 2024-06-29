## README.md（第一部分）

```markdown
# PDFCombineWithMenu

## Overview

This project provides a Python script for organizing PDF files and images into a directory structure based on their folder and file names. It also adds footers with page numbers of the same size to the first page or all pages of the PDFs and images.

本项目提供了一个Python脚本，用于根据文件夹和文件名将PDF文件和图像整理为目录结构，并在PDF和图像的首页或所有页面添加相同尺寸的页脚页码。

## Features

- **Organize PDFs and Images**: Automatically organize PDFs and images into a directory structure.
- **Add Footers**: Add footers with page numbers to PDFs and images.
- **Customizable**: Easily customize the footer size and page numbering options.

功能特点：

- **整理PDF和图像**：自动将PDF和图像整理为目录结构。
- **添加页脚**：在PDF和图像的页面添加页脚页码。
- **可定制**：轻松定制页脚大小和页码选项。

## Requirements

- Python 3.x
- PyPDF2
- PIL (Python Imaging Library)
- reportlab

安装要求：

- Python 3.x
- PyPDF2
- PIL（Python图像库）
- reportlab

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/PDFCombineWithMenu.git
   cd PDFCombineWithMenu
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

安装步骤：

1. 克隆仓库：

   ```bash
   git clone https://github.com/yourusername/PDFCombineWithMenu.git
   cd PDFCombineWithMenu
   ```

2. 安装所需的软件包：

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Organize PDFs and Images

To organize PDFs and images, run the script with the directory containing your files:

```bash
python organize_pdfs_and_images.py /path/to/your/files
```

### Add Footers

To add footers with page numbers to the first page or all pages of PDFs and images, use the following command:

```bash
python add_footers.py /path/to/your/files --all
```

For adding footers to the first page only:

```bash
python add_footers.py /path/to/your/files
```

使用方法：

### 整理PDF和图像

要整理PDF和图像，请运行脚本并提供包含文件的目录：

```bash
python organize_pdfs_and_images.py /path/to/your/files
```

### 添加页脚

要在PDF和图像的首页或所有页面添加页脚页码，请使用以下命令：

```bash
python add_footers.py /path/to/your/files --all
```

如果只在首页添加页脚：

```bash
python add_footers.py /path/to/your/files
```

## Script Details

### organize_pdfs_and_images.py

This script organizes PDFs and images into a directory structure based on their folder and file names.

- **Input**: Directory containing PDF files and images.
- **Output**: Organized directory structure.

### add_footers.py

This script adds footers with page numbers to PDFs and images. You can choose to add footers to the first page or all pages.

- **Input**: Directory containing PDF files and images.
- **Options**: 
  - `--all`: Add footers to all pages.
  - Default: Add footers to the first page only.
- **Output**: PDFs and images with added footers.

脚本详情：

### organize_pdfs_and_images.py

此脚本根据文件夹和文件名将PDF和图像整理为目录结构。

- **输入**：包含PDF文件和图像的目录。
- **输出**：整理后的目录结构。

### add_footers.py

此脚本在PDF和图像的页面添加页脚页码。你可以选择在首页或所有页面添加页脚。

- **输入**：包含PDF文件和图像的目录。
- **选项**：
  - `--all`：在所有页面添加页脚。
  - 默认：仅在首页添加页脚。
- **输出**：添加了页脚的PDF和图像。

## Examples

Here are some examples of how to use the scripts.

### Example 1: Organize Files

Suppose you have the following directory structure:

```
/path/to/your/files
├── folder1
│   ├── file1.pdf
│   ├── file2.jpg
├── folder2
│   ├── file3.pdf
│   ├── file4.png
```

To organize these files, run:

```bash
python organize_pdfs_and_images.py /path/to/your/files
```

### Example 2: Add Footers

To add footers with page numbers to all pages of PDFs and images:

```bash
python add_footers.py /path/to/your/files --all
```

示例：

### 示例1：整理文件

假设你有以下目录结构：

```
/path/to/your/files
├── folder1
│   ├── file1.pdf
│   ├── file2.jpg
├── folder2
│   ├── file3.pdf
│   ├── file4.png
```

要整理这些文件，运行：

```bash
python organize_pdfs_and_images.py /path/to/your/files
```

### 示例2：添加页脚

要在PDF和图像的所有页面添加页脚页码：

```bash
python add_footers.py /path/to/your/files --all
```

## Customization

You can customize the footer size and page numbering options by modifying the `add_footers.py` script. Look for the following sections in the script:

- **Footer Size**: Adjust the size of the footer by modifying the corresponding variables.
- **Page Numbering**: Customize the page numbering format and position.

自定义：

你可以通过修改 `add_footers.py` 脚本来自定义页脚大小和页码选项。请查找脚本中的以下部分：

- **页脚大小**：通过修改相应的变量来调整页脚的大小。
- **页码格式**：自定义页码的格式和位置。
好的，以下是 README 文件的第二部分：

## README.md（第二部分）

```markdown
## Directory Structure

After running the `organize_pdfs_and_images.py` script, the directory structure will be organized as follows:

```
/organized
├── folder1
│   ├── file1.pdf
│   ├── file2.jpg
├── folder2
│   ├── file3.pdf
│   ├── file4.png
```

Each folder will contain the corresponding PDFs and images organized by their original folder and file names.

目录结构：

运行 `organize_pdfs_and_images.py` 脚本后，目录结构将如下组织：

```
/organized
├── folder1
│   ├── file1.pdf
│   ├── file2.jpg
├── folder2
│   ├── file3.pdf
│   ├── file4.png
```

每个文件夹将包含按原文件夹和文件名整理的相应PDF和图像。

## Detailed Steps for Adding Footers

### Step 1: Load PDF and Image Files

The script first loads all PDF and image files from the specified directory.

### Step 2: Create Footer Template

A footer template is created using the `reportlab` library, which includes the page number.

### Step 3: Add Footer to PDFs

For each PDF, the script adds the footer template to the first page or all pages, based on the specified options.

### Step 4: Add Footer to Images

For each image, the script converts the image to PDF format (if not already a PDF), adds the footer template, and saves the result.

### Step 5: Save the Result

The modified PDFs and images are saved in the organized directory structure.

添加页脚的详细步骤：

### 第一步：加载PDF和图像文件

脚本首先从指定目录加载所有PDF和图像文件。

### 第二步：创建页脚模板

使用 `reportlab` 库创建页脚模板，其中包含页码。

### 第三步：将页脚添加到PDF

对于每个PDF，脚本根据指定的选项将页脚模板添加到首页或所有页面。

### 第四步：将页脚添加到图像

对于每个图像，脚本将图像转换为PDF格式（如果尚未转换），添加页脚模板，并保存结果。

### 第五步：保存结果

修改后的PDF和图像将保存到组织好的目录结构中。

## Example Code Snippets

Here are some example code snippets that demonstrate how to use the scripts.

### Example 1: Organize Files

```python
import os
from organize_pdfs_and_images import organize_files

# Specify the directory containing your files
directory = '/path/to/your/files'

# Organize the files
organize_files(directory)
```

### Example 2: Add Footers

```python
import os
from add_footers import add_footers

# Specify the directory containing your files
directory = '/path/to/your/files'

# Add footers to all pages
add_footers(directory, all_pages=True)

# Add footers to the first page only
add_footers(directory, all_pages=False)
```

代码示例：

### 示例1：整理文件

```python
import os
from organize_pdfs_and_images import organize_files

# 指定包含文件的目录
directory = '/path/to/your/files'

# 整理文件
organize_files(directory)
```

### 示例2：添加页脚

```python
import os
from add_footers import add_footers

# 指定包含文件的目录
directory = '/path/to/your/files'

# 在所有页面添加页脚
add_footers(directory, all_pages=True)

# 仅在首页添加页脚
add_footers(directory, all_pages=False)
```

## Troubleshooting

### Issue: Missing Fonts

If you encounter issues with missing fonts when adding footers, make sure you have the necessary fonts installed on your system. You can also specify a different font in the `add_footers.py` script.

### Issue: Unsupported File Formats

If you encounter issues with unsupported file formats, ensure that all files in the specified directory are either PDFs or images (JPG, PNG).

故障排除：

### 问题：缺少字体

如果在添加页脚时遇到字体缺失问题，请确保系统中已安装必要的字体。你也可以在 `add_footers.py` 脚本中指定不同的字体。

### 问题：不支持的文件格式

如果遇到不支持的文件格式问题，请确保指定目录中的所有文件都是PDF或图像（JPG，PNG）。

## Future Improvements

Here are some potential improvements for the project:

- **Enhanced Error Handling**: Improve error handling to provide more informative messages and handle edge cases.
- **Additional File Formats**: Add support for additional file formats.
- **GUI Interface**: Develop a graphical user interface for easier use.

未来改进：

以下是该项目的一些潜在改进：

- **增强错误处理**：改进错误处理以提供更有用的信息并处理边缘情况。
- **更多文件格式**：添加对更多文件格式的支持。
- **图形用户界面**：开发图形用户界面以便更容易使用。

## Contact

For any questions or issues, please contact [yourname] at [youremail@example.com].

联系方式：

如果有任何问题或疑问，请联系 [yourname]，邮箱 [youremail@example.com]。

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

许可证：

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。


这部分包含了项目的目录结构、详细的步骤说明、代码示例、故障排除、未来改进建议、联系信息和许可证声明。希望这些内容能帮助你更好地理解和使用这个项目。