import os
import re
import tempfile

import pypandoc
import streamlit as st

SITE = "https://viewmarkdown.com"

st.set_page_config(page_title="Markdown to Word Converter", page_icon="📝", layout="centered")

st.title("Markdown to Word Converter")
st.caption(f"by [ViewMarkdown.com]({SITE}/markdown-to-word)")

SAMPLE = """# Project update

Paste your Markdown here, or upload a .md file.

## Done this week

- Finished the **report** draft
- Reviewed the *budget*

| Item | Owner | Status |
| --- | --- | --- |
| Launch plan | Sam | Done |
| Press release | Priya | In review |
"""

uploaded = st.file_uploader("Upload a .md file", type=["md", "markdown", "txt"])
if uploaded is not None:
    text = uploaded.getvalue().decode("utf-8", errors="replace")
else:
    text = st.text_area("Markdown", value=SAMPLE, height=300, label_visibility="collapsed")


def title_of(markdown: str) -> str:
    heading = re.search(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", markdown, re.M)
    name = heading.group(1) if heading else "document"
    name = re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-").lower()
    return name[:60] or "document"


if text.strip():
    # pandoc writes binary formats to a file, so convert through a temp path.
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "out.docx")
        pypandoc.convert_text(text, "docx", format="gfm", outputfile=out)
        with open(out, "rb") as f:
            docx_bytes = f.read()

    st.download_button(
        "Download Word (.docx)",
        data=docx_bytes,
        file_name=f"{title_of(text)}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        type="primary",
    )

    st.subheader("Preview")
    st.markdown(text)

st.divider()
st.markdown(
    f"Free, no sign-up. For a live editor with PDF, HTML and share links, "
    f"use [ViewMarkdown.com]({SITE})."
)
