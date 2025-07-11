import pdfplumber
import docx

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_docx(file_path)
    elif file_path.endswith(".txt"):
        return extract_txt(file_path)
    return ""

def extract_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text.strip()

def extract_docx(file_path):
    text = ""
    try:
        doc = docx.Document(file_path)    #loads word document into an object
        text = "\n".join([para.text for para in doc.paragraphs])  #loops through each paragraph in word file, takes text, seperates using new line
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text.strip()   #returns cleaned text

def extract_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        print(f"Error reading TXT: {e}")
        return ""
