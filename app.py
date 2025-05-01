import streamlit as st
import zipfile
import os
import pandas as pd
import tempfile
import random
from pathlib import Path
import re
from textwrap import dedent
from main_pipeline import run_rag_pipeline
from parsers.parse_docs import parse_frameworks

# --- UI CONFIG ---
st.set_page_config(page_title="Compliance Gap Detector", layout="wide")

st.write("App is starting...")


# --- Title & Description ---
st.markdown(
    """
<h1 style='text-align: center; color: #00CFFD;'>CyberPulse Compliance Gap Dashboard</h1>
<p style='text-align: center; color: #EDEDED;'>Select frameworks and upload your policy documents to identify gaps.</p>
""",
    unsafe_allow_html=True,
)

# --- Select Frameworks First ---
st.markdown("### Select Compliance Framework(s):")

frameworks = [
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

for i, fw in enumerate(frameworks):
    if i % 3 == 0:
        if col1.checkbox(fw):
            selected_frameworks.append(fw)
    elif i % 3 == 1:
        if col2.checkbox(fw):
            selected_frameworks.append(fw)
    else:
        if col3.checkbox(fw):
            selected_frameworks.append(fw)
# --- Upload ZIP File ---
st.markdown("### Upload Your ZIP File")

uploaded_file = st.file_uploader(
    "Upload ZIP File Containing Policy Documents (.zip)", type="zip"
)

if uploaded_file is not None:

    # Define the target directory
    output_dir = Path("./data/policies")
    output_dir.mkdir(exist_ok=True)

    # Save the uploaded file temporarily
    zip_path = output_dir / "temp_upload.zip"
    with open(zip_path, "wb") as f:
        f.write(uploaded_file.read())

    # Unzip the file
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(output_dir)
    zip_path.unlink()


def parse_report(text):
    """
    Parse a text report of the form:

    *Requirement*:
    ...
    *Status*: ...
    *Reason*:
    ...
    *Target Policy*: ...

    into a list of dicts:
    [
      {
        "Requirement": "...",
        "Status": "...",
        "Reason": "...",
        "Target Policy": "..."
      },
      ...
    ]
    """
    entries = []

    # Split on each "*Requirement*:" (skip any leading text)
    blocks = re.split(r"\*Requirement\*:", text)[1:]

    for blk in blocks:
        # Requirement: up to *Status*:
        req, rest = re.split(r"\*Status\*:", blk, maxsplit=1)

        # Status: up to *Reason*:
        status, rest = re.split(r"\*Reason\*:", rest, maxsplit=1)

        # # Reason: up to *Target Policy*:
        # reason, rest = re.split(r'\*Target Policy\*[:]? ', rest, maxsplit=1)
        if "*Target Policy*" in rest:
            reason_text, target_text = re.split(
                r"\*Target Policy\*[:]? ?", rest, maxsplit=1
            )
        else:
            reason_text, target_text = rest, ""
        # Target Policy: up to end of block (or next *Requirement*, but split took care)
        # target = rest

        # Clean up whitespace and newlines
        clean = lambda s: dedent(s).strip().replace("\n", " ").replace("  ", " ")

        entries.append(
            {
                "Requirement": clean(req),
                "Status": clean(status),
                "Reason": clean(reason_text),
                "Target Policy": clean(target_text),
            }
        )

    return entries


# --- Display Results ---
if uploaded_file and selected_frameworks:
    print(selected_frameworks)
    # USE THE CODE THAT TAKES LIST OF FRAMEWORK NAMES AND OUTPUTS CONSISE REPORT HERE

    data = []

    with open("full_report.txt", "w", encoding="utf-8") as file:

        for x in selected_frameworks:
            concise_report = ""  # Initialize as string
            file.write("*" + x + "*" + "\n\n\n")
            frameworks = parse_frameworks(f"data/frameworks/{x}.xlsx")

            all_results = ""  # Collect all results for this framework
            for framework in frameworks:
                result = run_rag_pipeline(framework)
                file.write(result + "\n\n\n\n\n")
                all_results += result + "\n\n"  # Concatenate the results

            dict_report = parse_report(all_results)
            for dic in dict_report:
                data.append(
                    (
                        dic["Requirement"],
                        x,
                        dic["Status"],
                        dic["Reason"],
                        dic["Target Policy"],
                    )
                )

    # consise_report=main_code(selected_frameworks)
    # gap_and_status = [{"gap":"snigdh","status":"lol"}, {"gap":"sussy", "status":"fuhrer"}]

    # with tempfile.TemporaryDirectory() as tmp_dir:
    #     file_path = os.path.join(tmp_dir, uploaded_file.name)
    #     with open(file_path, "wb") as f:
    #         f.write(uploaded_file.getbuffer())

    #     with zipfile.ZipFile(file_path, 'r') as zip_ref:
    #         zip_ref.extractall(tmp_dir)

    #     st.success("ZIP uploaded and extracted successfully.")

    #     st.markdown(f"**Frameworks selected:** {', '.join(selected_frameworks)}")

    df = pd.DataFrame(
        data, columns=["Requirement", "Framework", "Status", "Reason", "Target Policy"]
    )

    st.markdown("### Compliance Gap Results")
    st.dataframe(df, use_container_width=True)
elif not uploaded_file:
    st.info("Please upload a ZIP file.")
elif not selected_frameworks:
    st.warning("Please select at least one compliance framework.")
