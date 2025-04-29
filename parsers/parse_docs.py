import os
import pandas as pd
import fitz
from docx import Document


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
                parsed_docs.append({"filename": filename, "content": text})
    return parsed_docs
