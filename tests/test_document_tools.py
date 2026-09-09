from backend.app.tools.document_tools import pdf_reader_tool


print("\n--- PDF READER TOOL TEST ---")

result = pdf_reader_tool.invoke(
    "data/uploads/sample.pdf"
)

print(result)