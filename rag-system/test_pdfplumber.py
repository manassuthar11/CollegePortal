import pdfplumber
import os

def test_pdfplumber_extraction():
    pdf_path = "documents/general/JECRC E-Brochure - 24-25.pdf"
    
    if not os.path.exists(pdf_path):
        print("PDF file not found!")
        return
    
    print(f"Testing PDF with pdfplumber: {pdf_path}")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Number of pages: {len(pdf.pages)}")
            
            all_text = ""
            for i, page in enumerate(pdf.pages[:5]):  # Test first 5 pages
                try:
                    text = page.extract_text()
                    if text:
                        print(f"Page {i+1}: {len(text)} characters extracted")
                        all_text += f"\n--- Page {i+1} ---\n{text}\n"
                    else:
                        print(f"Page {i+1}: No text extracted")
                        
                    # Also try to extract tables
                    tables = page.extract_tables()
                    if tables:
                        print(f"Page {i+1}: Found {len(tables)} tables")
                        for j, table in enumerate(tables):
                            all_text += f"\n--- Page {i+1} Table {j+1} ---\n"
                            for row in table:
                                if row:
                                    all_text += " | ".join([cell or "" for cell in row]) + "\n"
                                    
                except Exception as e:
                    print(f"Error processing page {i+1}: {e}")
            
            if all_text.strip():
                print(f"\nTotal extracted text: {len(all_text)} characters")
                print("\nFirst 500 characters:")
                print(all_text[:500])
                
                # Look for keywords
                keywords = ['fee', 'department', 'course', 'admission', 'facility', 'JECRC']
                found_keywords = []
                for keyword in keywords:
                    if keyword.lower() in all_text.lower():
                        found_keywords.append(keyword)
                
                print(f"\nFound keywords: {found_keywords}")
                
                # Save extracted text for review
                with open("extracted_text.txt", "w", encoding="utf-8") as f:
                    f.write(all_text)
                print("\nFull extracted text saved to 'extracted_text.txt'")
            else:
                print("\nNo text could be extracted from the PDF")
                
    except Exception as e:
        print(f"Error opening PDF: {e}")

if __name__ == "__main__":
    test_pdfplumber_extraction()