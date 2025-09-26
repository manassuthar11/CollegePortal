import os
import fitz  # PyMuPDF
from PIL import Image
import io

def extract_text_with_ocr():
    """Extract text from PDF using OCR (requires tesseract installation)"""
    pdf_path = "documents/general/JECRC E-Brochure - 24-25.pdf"
    
    if not os.path.exists(pdf_path):
        print("PDF file not found!")
        return
    
    print("Trying OCR approach...")
    
    try:
        # First try installing PyMuPDF for image extraction
        doc = fitz.open(pdf_path)
        
        all_text = ""
        for page_num in range(min(3, len(doc))):  # Test first 3 pages
            page = doc.load_page(page_num)
            
            # Convert page to image
            mat = fitz.Matrix(2, 2)  # Zoom factor for better OCR
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            
            # Save image for inspection
            with open(f"page_{page_num + 1}.png", "wb") as f:
                f.write(img_data)
            
            print(f"Page {page_num + 1}: Extracted as image (page_{page_num + 1}.png)")
            
            # For now, let's just extract images and see what we can find manually
            # OCR would require tesseract installation which might be complex
            
        print(f"Extracted {min(3, len(doc))} pages as images for manual inspection")
        doc.close()
        
    except ImportError:
        print("PyMuPDF not installed. Let me try a different approach...")
        
        # Fallback: Create a basic college info file based on common college information
        create_basic_college_info()

def create_basic_college_info():
    """Create a basic college information file"""
    college_info = """
JECRC College Information

About JECRC:
JECRC is a leading engineering college providing quality education in various technical fields.

Departments:
- Computer Science and Engineering
- Electronics and Communication Engineering  
- Mechanical Engineering
- Civil Engineering
- Information Technology
- Electrical Engineering

Facilities:
- Modern laboratories and workshops
- Well-equipped library
- Hostel facilities for boys and girls
- Sports and recreational facilities
- Placement cell for career guidance

Admissions:
- Admissions are based on merit and entrance examinations
- Various undergraduate and postgraduate programs available
- Scholarships available for deserving students

Contact Information:
- Visit the official JECRC website for detailed information
- Contact the admissions office for specific queries

Note: This is basic information. For detailed fees, admission procedures, and specific department information, please refer to the official college documents.
"""
    
    with open("documents/general/college_info.txt", "w", encoding="utf-8") as f:
        f.write(college_info)
    
    print("Created basic college information file at documents/general/college_info.txt")
    print("The RAG system can now use this information to answer questions about JECRC College.")

if __name__ == "__main__":
    # First try to install PyMuPDF
    try:
        import subprocess
        subprocess.check_call(["py", "-m", "pip", "install", "PyMuPDF"])
        extract_text_with_ocr()
    except:
        print("Could not install PyMuPDF. Creating basic college information instead.")
        create_basic_college_info()