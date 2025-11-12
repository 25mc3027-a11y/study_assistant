import fitz  # This is the PyMuPDF library
import io

def extract_text_from_pdf(pdf_file_bytes):
    """
    Extracts text from the bytes of a PDF file.
    'pdf_file_bytes' is the raw bytes from a file (e..g., from st.file_uploader.read()).
    """
    try:
        # Open the PDF from bytes
        with fitz.open(stream=pdf_file_bytes, filetype="pdf") as pdf_document:
            full_text = ""
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                full_text += page.get_text()
            
            if not full_text.strip():
                raise ValueError("No text found in PDF. The file might be image-based or empty.")
                
            return full_text
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        # Re-raise the exception to be caught by the UI
        raise ValueError(f"Failed to read PDF. Is it a valid file? Error: {e}")