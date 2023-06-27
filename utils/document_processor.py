# File: /cherryAI/utils/document_processor.py

from PyPDF2 import PdfFileReader

def read_pdf(file_path):
    """
    Reads a PDF file and returns its content.

    Parameters:
    file_path (str): The path to the PDF file.

    Returns:
    str: The content of the PDF file, or None if the file could not be read.
    """
    try:
        with open(file_path, 'rb') as file:
            pdf = PdfFileReader(file)
            text = ''
            for page in range(pdf.getNumPages()):
                text += pdf.getPage(page).extractText()
        return text
    except:
        return None
