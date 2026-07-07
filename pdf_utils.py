from pypdf import PdfReader
import io


def extract_text(uploaded_file) -> str:
    """Extract plain text from an uploaded PDF (Streamlit UploadedFile)."""
    if uploaded_file is None:
        return ""
    reader = PdfReader(io.BytesIO(uploaded_file.getvalue()))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
        text += "\n"
    return text.strip()