import fitz  # PyMuPDF

async def extract_text_from_pdf(file):
    content = await file.read()
    try:
        doc = fitz.open(stream=content, filetype="pdf")
    except Exception as e:
        raise ValueError(f"Could not open PDF: {str(e)}")

    text = ""
    for page in doc:
        text += page.get_text()
    return text