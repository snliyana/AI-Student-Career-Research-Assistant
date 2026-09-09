from langchain_core.tools import tool
from pypdf import PdfReader
import os


@tool
def pdf_reader_tool(file_path: str) -> str:
    """
    Read and extract text from a PDF document.

    Useful for:
    - Resume analysis
    - Job description analysis
    - Research paper reading
    - Career document summarization
    """

    try:
        if not os.path.exists(file_path):
            return f"PDF file not found: {file_path}"

        reader = PdfReader(file_path)

        extracted_text = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                extracted_text.append(text)

        if not extracted_text:
            return "No readable text was found in the PDF."

        full_text = "\n".join(extracted_text)

        # Limit output to avoid sending huge documents to the LLM
        max_chars = 6000

        if len(full_text) > max_chars:
            full_text = full_text[:max_chars]
            full_text += "\n\n[Document truncated for processing.]"

        return full_text

    except Exception as e:
        return (
            "PDF reading failed. "
            f"Error: {str(e)}"
        )