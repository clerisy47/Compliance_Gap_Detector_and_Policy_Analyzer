import os
import pandas as pd
import fitz
from docx import Document
from PIL import Image
import io
import pytesseract
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt_tab')



def parse_answer_library(path):
    df = pd.read_excel(path)
    entries = []
    for _, row in df.iterrows():
        entries.append(
            {
                "question": str(row.get("question", "")).strip(),
                "answer": str(row.get("answer", "")).strip(),
                "details": str(row.get("details", "")).strip(),
                "category": str(row.get("category", "")).strip(),
                "product": str(row.get("product_name", "")).strip(),
            }
        )
    return entries


def parse_frameworks(path):
    df = pd.read_excel(path)
    return [
        str(row["Statement"]).strip()
        for _, row in df.iterrows()
        if pd.notna(row["Statement"])
    ]


def parse_policy_folder(folder_path):
    parsed_docs = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            path = os.path.join(folder_path, filename)
            with fitz.open(path) as doc:
                text = "\n".join([page.get_text() for page in doc])
                sentences = sent_tokenize(text)
                parsed_docs.extend(sentences)
    return parsed_docs


# def parse_policy_folder(folder_path):
#     parsed_docs = []

#     for filename in os.listdir(folder_path):
#         if filename.lower().endswith(".pdf"):
#             path = os.path.join(folder_path, filename)
#             full_text = []

#             with fitz.open(path) as doc:
#                 for page_index in range(doc.page_count):
#                     page = doc.load_page(page_index)
#                     text = page.get_text()
#                     full_text.append(text)

#                     # Extract images and perform OCR
#                     image_list = page.get_images(full=True)
#                     for img_index, img in enumerate(image_list):
#                         xref = img[0]
#                         base_image = doc.extract_image(xref)
#                         image_bytes = base_image["image"]

#                         # grayscale conversion for better accuracy
#                         image = Image.open(io.BytesIO(image_bytes)).convert("L")
#                         ocr_text = pytesseract.image_to_string(image)
#                         if ocr_text.strip():
#                             full_text.append(
#                                 f"[Image {img_index + 1} OCR]: {ocr_text.strip()}"
#                             )

#             parsed_docs.append(
#                 {"filename": filename, "content": "\n".join(full_text).strip()}
#             )

#     return parsed_docs
