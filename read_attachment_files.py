import os
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document
import easyocr
import json
import openpyxl

# This modules is capable in reading any kind of image but is slow without a GPU. This works with EasyOCR GPU based OCR
# So if you have a GPU this works pretty fast.

def clear_all_files_folder(folder_path="attachments"):
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted: {filename}")
            except Exception as e:
                print(f"Failed to delete {filename}: {e}")
    print(f"All files cleared from '{folder_path}'")

def read_excel_file(file_path):
    try:
        sheets = pd.read_excel(file_path, sheet_name=None)
        sheets_data = {}
        for sheet_name, df in sheets.items():
            sheets_data[sheet_name] = df.fillna('').to_dict(orient='records')
        return json.dumps(sheets_data, indent=2)
    except Exception as err:
        return f"Error reading Excel file: {err}"

def read_csv_file(file_path):
    try:
        df = pd.read_csv(file_path)
        records = df.fillna('').to_dict(orient='records')
        return json.dumps(records, indent=2)
    except Exception as err:
        return f"Error reading CSV file: {err}"

def read_pdf_file(file_path):
    try:
        pdf_reader = PdfReader(file_path)
        pages_text = []
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text)
        return "\n".join(pages_text)
    except Exception as err:
        return f"Error reading PDF file: {err}"

def read_docx_file(file_path):
    try:
        document = Document(file_path)
        paragraphs = [para.text for para in document.paragraphs]
        return "\n".join(paragraphs)
    except Exception as err:
        return f"Error reading DOCX file: {err}"

def read_doc_file(file_path):
    try:
        import subprocess
        process = subprocess.run(['antiword', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if process.returncode == 0:
            return process.stdout
        else:
            return "antiword failed or not installed."
    except Exception as err:
        return f"Error reading DOC file: {err}"

def read_image_file(file_path):
    # Initialize EasyOCR without CUDA (CPU only)
    ocr_reader = easyocr.Reader(['en'], gpu=False)  # set gpu=True for CUDA-enabled GPU
    try:
        text_lines = ocr_reader.readtext(file_path, detail=0)
        return "\n".join(text_lines)
    except Exception as err:
        return f"Error reading image file: {err}"

def read_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.xls', '.xlsx']:
        return read_excel_file(file_path)
    elif ext == '.csv':
        return read_csv_file(file_path)
    elif ext == '.pdf':
        return read_pdf_file(file_path)
    elif ext == '.docx':
        return read_docx_file(file_path)
    elif ext == '.doc':
        return read_doc_file(file_path)
    elif ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif']:
        return read_image_file(file_path)
    
    else:
        return f"Unsupported file type: {ext}"

def extract_all_files_from_folder(folder_path="attachments"):
    extracted_data = []
    # Read all files one by one in attachments
    for fname in os.listdir(folder_path):
        fpath = os.path.join(folder_path, fname)
        if os.path.isfile(fpath):
            print(f"Processing {fname}...")
            text = read_file(fpath)
            extracted_data.append({
                "filename": fname,
                "text": text
            })
    return extracted_data


if __name__ == "__main__":
    # All kinds of attachments works seamlessly
    attachments_folder = "Test All Kinds of Attachments"
    extracted_texts = extract_all_files_from_folder(attachments_folder)
    
    for file_data in extracted_texts:
        filename = file_data.get('filename')
        text_content = file_data.get('text')
        
        print(f"\n--- Text extracted from {filename} ---\n")
        print(text_content)
        print("\n" + "="*40 + "\n")

