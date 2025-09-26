import fitz  # PyMuPDF
import easyocr
import cv2
import numpy as np
from PIL import Image
import io
import os

def extract_text_from_jecrc_pdf():
    """Extract text from JECRC E-Brochure PDF using OCR"""
    
    pdf_path = "documents/general/JECRC E-Brochure - 24-25.pdf"
    
    if not os.path.exists(pdf_path):
        print("❌ JECRC PDF not found!")
        return None
    
    print("🚀 Starting OCR extraction from JECRC E-Brochure...")
    print("📄 Processing PDF with advanced image recognition...")
    
    try:
        # Initialize EasyOCR reader for English
        reader = easyocr.Reader(['en'])
        
        # Open PDF
        doc = fitz.open(pdf_path)
        print(f"📚 PDF loaded: {len(doc)} pages")
        
        all_extracted_text = ""
        successful_pages = 0
        
        # Process each page (limit to first 10 pages for now to avoid long processing time)
        max_pages = min(10, len(doc))
        print(f"🔍 Processing first {max_pages} pages with OCR...")
        
        for page_num in range(max_pages):
            try:
                print(f"\n📄 Processing page {page_num + 1}/{max_pages}...")
                
                # Get page
                page = doc.load_page(page_num)
                
                # Convert to high-resolution image (zoom for better OCR)
                mat = fitz.Matrix(2, 2)  # 2x zoom for better quality
                pix = page.get_pixmap(matrix=mat)
                
                # Convert to numpy array
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                img_array = np.array(img)
                
                # Convert RGB to BGR for OpenCV
                if len(img_array.shape) == 3:
                    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                
                # Enhance image for better OCR
                # Convert to grayscale
                gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
                
                # Apply adaptive thresholding to improve text clarity
                processed = cv2.adaptiveThreshold(
                    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
                )
                
                # Use EasyOCR to extract text
                print("🔤 Running OCR on page...")
                results = reader.readtext(processed)
                
                # Extract text from results
                page_text = ""
                for (bbox, text, conf) in results:
                    if conf > 0.3:  # Only include text with confidence > 30%
                        page_text += text + " "
                
                if page_text.strip():
                    print(f"✅ Page {page_num + 1}: Extracted {len(page_text)} characters")
                    all_extracted_text += f"\n=== PAGE {page_num + 1} ===\n{page_text}\n"
                    successful_pages += 1
                else:
                    print(f"⚠️ Page {page_num + 1}: No text extracted")
                    
            except Exception as e:
                print(f"❌ Error processing page {page_num + 1}: {e}")
        
        doc.close()
        
        print(f"\n🎯 OCR Processing Complete!")
        print(f"✅ Successfully processed: {successful_pages}/{max_pages} pages")
        print(f"📝 Total extracted text: {len(all_extracted_text)} characters")
        
        if all_extracted_text.strip():
            # Save extracted text
            with open("jecrc_extracted_text.txt", "w", encoding="utf-8") as f:
                f.write(f"JECRC College Information (OCR Extracted)\n")
                f.write(f"Extracted from: {pdf_path}\n")
                f.write(f"Pages processed: {successful_pages}/{max_pages}\n")
                f.write(f"Total characters: {len(all_extracted_text)}\n")
                f.write("=" * 50 + "\n\n")
                f.write(all_extracted_text)
            
            print(f"💾 Extracted text saved to: jecrc_extracted_text.txt")
            
            # Preview first 500 characters
            preview = all_extracted_text.replace('\n', ' ')[:500]
            print(f"\n📖 Preview of extracted text:")
            print("-" * 50)
            print(preview + "...")
            print("-" * 50)
            
            return all_extracted_text
        else:
            print("❌ No text could be extracted from the PDF pages")
            return None
            
    except Exception as e:
        print(f"❌ Error during OCR processing: {e}")
        return None

if __name__ == "__main__":
    print("🎓 JECRC PDF OCR Text Extraction")
    print("=" * 40)
    
    extracted_text = extract_text_from_jecrc_pdf()
    
    if extracted_text:
        print("\n🎉 SUCCESS: Text extracted from JECRC PDF!")
        print("📁 File saved as: jecrc_extracted_text.txt")
        print("🔄 Next step: Update RAG system to use this extracted text")
    else:
        print("\n❌ FAILED: Could not extract text from JECRC PDF")
        print("💡 The PDF might be heavily image-based or encrypted")