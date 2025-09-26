import PyPDF2
import os

def test_pdf_extraction():
    pdf_path = "documents/general/JECRC E-Brochure - 24-25.pdf"
    
    if not os.path.exists(pdf_path):
        print("PDF file not found!")
        return
    
    print(f"Testing PDF: {pdf_path}")
    print(f"File size: {os.path.getsize(pdf_path)} bytes")
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            print(f"Number of pages: {len(pdf_reader.pages)}")
            
            # Try to extract text from first few pages
            for i in range(min(3, len(pdf_reader.pages))):
                try:
                    page = pdf_reader.pages[i]
                    text = page.extract_text()
                    print(f"Page {i+1} text length: {len(text)}")
                    if text:
                        print(f"First 200 chars: {text[:200]}")
                        print("---")
                    else:
                        print("No text extracted from this page")
                except Exception as e:
                    print(f"Error extracting page {i+1}: {e}")
                    
    except Exception as e:
        print(f"Error opening PDF: {e}")

if __name__ == "__main__":
    test_pdf_extraction()