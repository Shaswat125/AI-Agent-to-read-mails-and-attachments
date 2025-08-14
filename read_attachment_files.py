import os
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document
import pytesseract
from PIL import Image
import json

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
    try:
        # Open image with PIL
        img = Image.open(file_path)
        # Use pytesseract to do OCR on the image
        text = pytesseract.image_to_string(img)
        return text
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
    all_texts = {}
    for fname in os.listdir(folder_path):
        fpath = os.path.join(folder_path, fname)
        if os.path.isfile(fpath):
            print(f"Processing {fname}...")
            all_texts[fname] = read_file(fpath)
    return all_texts

if __name__ == "__main__":
    attachments_folder = "attachments"
    extracted_texts = extract_all_files_from_folder(attachments_folder)
    for filename, text_content in extracted_texts.items():
        print(f"\n--- Text extracted from {filename} ---\n")
        print(text_content[:])
        print("\n" + "="*40 + "\n")

