import fitz  # PyMuPDF

async def extract_text_from_pdf(file):
    doc = fitz.open(stream=await file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text