import streamlit as st
import zipfile
import os
import pandas as pd
from pathlib import Path
import re
from textwrap import dedent
from main_pipeline import run_rag_pipeline

from parsers.parse_docs import (
    parse_frameworks,
    parse_policy_folder,
)


# --- UI CONFIG ---
st.set_page_config(page_title="Compliance Gap Detector", layout="wide")
st.markdown(
    """
    <h1 style='text-align: center; color: #00CFFD;'>CyberPulse Compliance Gap Dashboard</h1>
    <p style='text-align: center; color: #EDEDED;'>Select frameworks and upload your policy documents to identify gaps.</p>
    """,
    unsafe_allow_html=True,
)

# --- Framework Selection ---
st.markdown("### Select Compliance Framework(s):")

available_frameworks = [
    "ISO",
    "NIST 800-53",
    "HIPAA",
    "GDPR",
    "CCPA",
    "PCI-DSS",
    "CIS",
    "HITRUST",
    "NIST CSF",
    "SCF",
]

col1, col2, col3 = st.columns(3)
selected_frameworks = []

for i, fw in enumerate(available_frameworks):
    col = [col1, col2, col3][i % 3]
    if col.checkbox(fw):
        selected_frameworks.append(fw)

# --- ZIP File Upload ---
st.markdown("### Upload Your ZIP File")
uploaded_file = st.file_uploader(
    "Upload ZIP File Containing Policy Documents (.zip)", type="zip"
)

if uploaded_file is not None:
    output_dir = Path("./data/policies")
    output_dir.mkdir(parents=True, exist_ok=True)

    zip_path = output_dir / "temp_upload.zip"
    with open(zip_path, "wb") as f:
        f.write(uploaded_file.read())

    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(output_dir)
        zip_path.unlink()
        st.success("ZIP uploaded and extracted successfully.")
    except zipfile.BadZipFile:
        st.error("Uploaded file is not a valid ZIP archive.")
        st.stop()


def parse_report(text):
    entries = []
    blocks = re.split(r"\*Requirement\*:", text)[1:]

    for blk in blocks:
        try:
            req, rest = re.split(r"\*Status\*:", blk, maxsplit=1)
            status, rest = re.split(r"\*Reason\*:", rest, maxsplit=1)
            if "*Target Policy*" in rest:
                reason_text, target_text = re.split(
                    r"\*Target Policy\*[:]? ?", rest, maxsplit=1
                )
            else:
                reason_text, target_text = rest, ""

            clean = lambda s: dedent(s).strip().replace("\n", " ").replace("  ", " ")
            entries.append(
                {
                    "Requirement": clean(req),
                    "Status": clean(status),
                    "Reason": clean(reason_text),
                    "Target Policy": clean(target_text),
                }
            )
        except ValueError as e:
            st.warning(f"Skipping a block due to parsing error: {e}")
            continue

    return entries


policies = parse_policy_folder("data/policies/")


# --- Run Analysis ---
if uploaded_file and selected_frameworks:
    st.markdown(f"**Frameworks selected:** {', '.join(selected_frameworks)}")
    results_data = []

    with open("full_report.txt", "w", encoding="utf-8") as report_file:
        for framework_name in selected_frameworks:
            st.write(f"Processing: **{framework_name}**")
            report_file.write(f"*{framework_name}*\n\n\n")
            try:
                parsed_frameworks = parse_frameworks(
                    f"data/frameworks/{framework_name}.xlsx"
                )
            except Exception as e:
                st.error(f"Error loading framework {framework_name}: {e}")
                continue

            full_text = ""
            for fw in parsed_frameworks:
                try:
                    result = run_rag_pipeline(fw, policies)
                    report_file.write(result + "\n\n\n")
                    full_text += result + "\n\n"
                except Exception as e:
                    st.error(
                        f"Error running pipeline for {fw.get('name', 'unknown')}: {e}"
                    )

            parsed_data = parse_report(full_text)
            for item in parsed_data:
                results_data.append(
                    (
                        item["Requirement"],
                        framework_name,
                        item["Status"],
                        item["Reason"],
                        item["Target Policy"],
                    )
                )

    if results_data:
        df = pd.DataFrame(
            results_data,
            columns=["Requirement", "Framework", "Status", "Reason", "Target Policy"],
        )
        st.markdown("### Compliance Gap Results")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No data to display. There may have been errors during processing.")

elif not uploaded_file:
    st.info("Please upload a ZIP file.")
elif not selected_frameworks:
    st.warning("Please select at least one compliance framework.")
