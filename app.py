import os
import re
import tempfile

import pypandoc
import streamlit as st

SITE = "https://viewmarkdown.com"

st.set_page_config(page_title="Markdown to Word Converter", page_icon="📝", layout="wide")

st.title("Markdown to Word Converter")
st.markdown(f"### by [ViewMarkdown.com]({SITE}/markdown-to-word)")

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


def title_of(markdown: str) -> str:
    heading = re.search(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", markdown, re.M)
    name = heading.group(1) if heading else "document"
    name = re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-").lower()
    return name[:60] or "document"


def to_docx(markdown: str) -> bytes:
    # pandoc writes binary formats to a file, so convert through a temp path.
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "out.docx")
        pypandoc.convert_text(markdown, "docx", format="gfm", outputfile=out)
        with open(out, "rb") as f:
            return f.read()


uploaded = st.file_uploader("Upload a .md file", type=["md", "markdown", "txt"])
if uploaded is not None:
    st.session_state["md"] = uploaded.getvalue().decode("utf-8", errors="replace")
if "md" not in st.session_state:
    st.session_state["md"] = SAMPLE

left, right = st.columns(2, gap="large")

with left:
    st.markdown("**Markdown**")
    text = st.text_area(
        "Markdown",
        key="md",
        height=520,
        label_visibility="collapsed",
        help="The preview updates when you click outside the box or press Cmd/Ctrl+Enter.",
    )

with right:
    st.markdown("**Preview**")
    with st.container(border=True, height=520):
        st.markdown(text)

if text.strip():
    st.download_button(
        "Download Word (.docx)",
        data=to_docx(text),
        file_name=f"{title_of(text)}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        type="primary",
    )

st.divider()
st.markdown(
    f"Free, no sign-up. For a live editor with PDF, HTML and share links, "
    f"use [ViewMarkdown.com]({SITE})."
)
