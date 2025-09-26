"""
Real Document Information Extractor for JECRC College Portal
===============================================

This system extracts ONLY genuine information from your actual documents.
No synthetic data, no assumptions, no fabricated content.

Key Features:
- Advanced OCR with multiple preprocessing techniques
- Multi-layer text extraction (direct PDF + OCR)
- Intelligent information categorization
- Context-aware extraction patterns
- Quality scoring for extracted information

Author: College Portal Team
Date: September 2025
"""

import fitz  # PyMuPDF
import easyocr
import cv2
import numpy as np
from PIL import Image
import io
import os
import re
import json
from collections import defaultdict
from datetime import datetime

class RealDocumentExtractor:
    def __init__(self):
        self.ocr_reader = None
        self.extracted_data = {
            'fee_information': [],
            'academic_programs': [],
            'facilities': [],
            'placement_info': [],
            'contact_details': [],
            'admission_info': [],
            'raw_pages': {},
            'extraction_metadata': {
                'timestamp': datetime.now().isoformat(),
                'confidence_threshold': 0.6,
                'pages_processed': 0,
                'extraction_method': 'hybrid_ocr_direct'
            }
        }
    
    def setup_ocr(self):
        """Initialize OCR engine"""
        if self.ocr_reader is None:
            print("🔧 Initializing OCR engine...")
            self.ocr_reader = easyocr.Reader(['en'], gpu=False)
            print("✅ OCR ready")
    
    def enhance_image_quality(self, image):
        """Apply advanced image preprocessing for better OCR accuracy"""
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Noise reduction
        denoised = cv2.medianBlur(gray, 3)
        
        # Enhance contrast using CLAHE
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        # Adaptive thresholding
        binary = cv2.adaptiveThreshold(
            enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Morphological operations to clean text
        kernel = np.ones((1,1), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        
        return cleaned
    
    def extract_from_pdf_page(self, page, page_number):
        """Extract text using both direct PDF reading and OCR"""
        extracted_content = {
            'page_num': page_number,
            'direct_text': '',
            'ocr_text': '',
            'combined_text': '',
            'confidence_score': 0.0
        }
        
        # Method 1: Direct text extraction from PDF
        try:
            direct_text = page.get_text().strip()
            if direct_text and len(direct_text) > 20:
                extracted_content['direct_text'] = direct_text
                print(f"Page {page_number}: Direct extraction - {len(direct_text)} chars")
        except Exception as e:
            print(f"Page {page_number}: Direct extraction failed - {e}")
        
        # Method 2: OCR extraction
        try:
            # Convert to high-resolution image
            zoom = 3  # Higher resolution for better OCR
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            
            # Convert to PIL then numpy array
            pil_image = Image.open(io.BytesIO(img_data))
            img_array = np.array(pil_image)
            
            # Convert RGB to BGR for OpenCV
            if len(img_array.shape) == 3:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # Enhance image quality
            processed_image = self.enhance_image_quality(img_array)
            
            # Perform OCR
            ocr_results = self.ocr_reader.readtext(processed_image, detail=1)
            
            # Process OCR results
            page_text = ""
            confidences = []
            
            for (bbox, text, confidence) in ocr_results:
                if confidence > 0.5 and len(text.strip()) > 2:  # Quality filtering
                    page_text += text.strip() + " "
                    confidences.append(confidence)
            
            if page_text.strip():
                extracted_content['ocr_text'] = page_text.strip()
                extracted_content['confidence_score'] = np.mean(confidences) if confidences else 0
                print(f"Page {page_number}: OCR extraction - {len(page_text)} chars (conf: {extracted_content['confidence_score']:.2f})")
            
        except Exception as e:
            print(f"Page {page_number}: OCR extraction failed - {e}")
        
        # Combine texts intelligently
        combined = ""
        if extracted_content['direct_text']:
            combined += extracted_content['direct_text'] + "\n"
        if extracted_content['ocr_text'] and extracted_content['ocr_text'] not in combined:
            combined += extracted_content['ocr_text']
        
        extracted_content['combined_text'] = combined.strip()
        return extracted_content
    
    def extract_fee_information(self, text, page_num, confidence):
        """Extract fee-related information with context"""
        fee_patterns = [
            # Various fee patterns
            (r'fee[s]?\s*[:\-]?\s*(?:₹|rs\.?|inr)?\s*(\d+(?:,\d+)*(?:\.\d+)?)', 'general_fee'),
            (r'tuition\s*fee[s]?\s*[:\-]?\s*(?:₹|rs\.?|inr)?\s*(\d+(?:,\d+)*(?:\.\d+)?)', 'tuition'),
            (r'admission\s*fee[s]?\s*[:\-]?\s*(?:₹|rs\.?|inr)?\s*(\d+(?:,\d+)*(?:\.\d+)?)', 'admission'),
            (r'hostel\s*fee[s]?\s*[:\-]?\s*(?:₹|rs\.?|inr)?\s*(\d+(?:,\d+)*(?:\.\d+)?)', 'hostel'),
            (r'mess\s*fee[s]?\s*[:\-]?\s*(?:₹|rs\.?|inr)?\s*(\d+(?:,\d+)*(?:\.\d+)?)', 'mess'),
            (r'transport\s*fee[s]?\s*[:\-]?\s*(?:₹|rs\.?|inr)?\s*(\d+(?:,\d+)*(?:\.\d+)?)', 'transport'),
            (r'(?:₹|rs\.?|inr)\s*(\d+(?:,\d+)*(?:\.\d+)?)', 'currency_amount')
        ]
        
        for pattern, fee_type in fee_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                amount = match.group(1)
                # Only consider reasonable fee amounts (1000 to 10,00,000)
                amount_num = int(amount.replace(',', '').split('.')[0])
                if 1000 <= amount_num <= 1000000:
                    # Extract context around the match
                    start = max(0, match.start() - 100)
                    end = min(len(text), match.end() + 100)
                    context = text[start:end].strip()
                    
                    self.extracted_data['fee_information'].append({
                        'amount': amount,
                        'type': fee_type,
                        'context': context,
                        'page': page_num,
                        'confidence': confidence,
                        'raw_match': match.group(0)
                    })
    
    def extract_academic_programs(self, text, page_num, confidence):
        """Extract academic program information"""
        program_patterns = [
            r'b\.?tech\.?\s+(?:in\s+)?([a-z\s&]+(?:engineering|science|technology))',
            r'bachelor\s+of\s+technology\s+(?:in\s+)?([a-z\s&]+)',
            r'computer\s+science\s+(?:and\s+|&\s+)?engineering',
            r'electronics?\s+(?:and\s+|&\s+)?communication\s+engineering',
            r'mechanical\s+engineering',
            r'civil\s+engineering',
            r'electrical\s+engineering',
            r'information\s+technology',
            r'artificial\s+intelligence',
            r'data\s+science'
        ]
        
        for pattern in program_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                program_name = match.group(0).strip()
                if len(program_name) > 5:  # Reasonable program name length
                    # Extract context
                    start = max(0, match.start() - 80)
                    end = min(len(text), match.end() + 80)
                    context = text[start:end].strip()
                    
                    self.extracted_data['academic_programs'].append({
                        'program_name': program_name.title(),
                        'context': context,
                        'page': page_num,
                        'confidence': confidence
                    })
    
    def extract_contact_information(self, text, page_num, confidence):
        """Extract contact details"""
        contact_patterns = [
            (r'(?:phone|tel|contact|mob|mobile)[:\s]*(\+?\d{1,4}[-\s]?\d{3,4}[-\s]?\d{6,10})', 'phone'),
            (r'(?:email|e-mail)[:\s]*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', 'email'),
            (r'(?:website|www)[:\s]*((?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', 'website'),
            (r'(?:address|located|location)[:\s]*([^\n]{20,100})', 'address')
        ]
        
        for pattern, contact_type in contact_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                contact_info = match.group(1).strip()
                if len(contact_info) > 3:
                    # Extract context
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end].strip()
                    
                    self.extracted_data['contact_details'].append({
                        'info': contact_info,
                        'type': contact_type,
                        'context': context,
                        'page': page_num,
                        'confidence': confidence
                    })
    
    def extract_placement_information(self, text, page_num, confidence):
        """Extract placement and company information"""
        # Common company names and placement keywords
        placement_keywords = ['placement', 'recruit', 'package', 'salary', 'job', 'career']
        
        if any(keyword in text.lower() for keyword in placement_keywords):
            # Extract company names
            company_patterns = [
                r'\b(tcs|infosys|wipro|accenture|microsoft|google|amazon|adobe|ibm|cognizant|capgemini)\b',
                r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:ltd|limited|inc|corp|pvt)\.?))\b'
            ]
            
            for pattern in company_patterns:
                companies = re.finditer(pattern, text, re.IGNORECASE)
                for match in companies:
                    company_name = match.group(0).strip()
                    if len(company_name) > 2:
                        # Extract context
                        start = max(0, match.start() - 100)
                        end = min(len(text), match.end() + 100)
                        context = text[start:end].strip()
                        
                        self.extracted_data['placement_info'].append({
                            'company': company_name,
                            'context': context,
                            'page': page_num,
                            'confidence': confidence
                        })
            
            # Extract package information
            package_patterns = [
                r'(?:package|salary|ctc)[:\s]*(?:₹|rs\.?|inr)?\s*(\d+(?:\.\d+)?\s*(?:lpa|lakhs?))',
                r'(?:₹|rs\.?|inr)\s*(\d+(?:\.\d+)?\s*(?:lpa|lakhs?))',
                r'(\d+(?:\.\d+)?)\s*(?:lpa|lakhs?\s*per\s*annum)'
            ]
            
            for pattern in package_patterns:
                packages = re.finditer(pattern, text, re.IGNORECASE)
                for match in packages:
                    package_info = match.group(1)
                    # Extract context
                    start = max(0, match.start() - 100)
                    end = min(len(text), match.end() + 100)
                    context = text[start:end].strip()
                    
                    self.extracted_data['placement_info'].append({
                        'package': package_info,
                        'context': context,
                        'page': page_num,
                        'confidence': confidence
                    })
    
    def process_document(self, pdf_path):
        """Main document processing function"""
        if not os.path.exists(pdf_path):
            print(f"❌ Document not found: {pdf_path}")
            return False
        
        self.setup_ocr()
        print(f"📄 Processing: {pdf_path}")
        
        try:
            doc = fitz.open(pdf_path)
            total_pages = len(doc)
            print(f"📚 Document has {total_pages} pages")
            
            successful_extractions = 0
            total_text_length = 0
            
            for page_idx in range(min(total_pages, 20)):  # Process up to 20 pages
                page = doc.load_page(page_idx)
                page_num = page_idx + 1
                
                print(f"\n🔍 Processing page {page_num}...")
                
                # Extract content from page
                page_content = self.extract_from_pdf_page(page, page_num)
                
                if page_content['combined_text']:
                    # Store raw page content
                    self.extracted_data['raw_pages'][page_num] = page_content
                    
                    # Extract structured information
                    text = page_content['combined_text']
                    confidence = page_content['confidence_score']
                    
                    self.extract_fee_information(text, page_num, confidence)
                    self.extract_academic_programs(text, page_num, confidence)
                    self.extract_contact_information(text, page_num, confidence)
                    self.extract_placement_information(text, page_num, confidence)
                    
                    successful_extractions += 1
                    total_text_length += len(text)
                    print(f"✅ Page {page_num}: {len(text)} characters extracted")
                else:
                    print(f"⚠️ Page {page_num}: No usable text found")
            
            doc.close()
            
            # Update metadata
            self.extracted_data['extraction_metadata'].update({
                'pages_processed': successful_extractions,
                'total_pages': total_pages,
                'total_text_length': total_text_length,
                'processing_complete': True
            })
            
            print(f"\n🎯 Extraction Complete!")
            print(f"✅ Pages processed: {successful_extractions}/{total_pages}")
            print(f"📊 Total text extracted: {total_text_length} characters")
            print(f"💰 Fee instances found: {len(self.extracted_data['fee_information'])}")
            print(f"🎓 Programs identified: {len(self.extracted_data['academic_programs'])}")
            print(f"📞 Contact details: {len(self.extracted_data['contact_details'])}")
            print(f"🏢 Placement references: {len(self.extracted_data['placement_info'])}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error processing document: {e}")
            return False
    
    def generate_knowledge_base(self):
        """Generate knowledge base from extracted real data only"""
        
        kb = f"""JECRC College Information - Real Document Extraction
========================================================

Extraction Summary:
- Timestamp: {self.extracted_data['extraction_metadata']['timestamp']}
- Pages Processed: {self.extracted_data['extraction_metadata'].get('pages_processed', 0)}
- Total Characters: {self.extracted_data['extraction_metadata'].get('total_text_length', 0)}
- Method: Advanced OCR + Direct PDF Text Extraction
- Data Source: Actual JECRC E-Brochure PDF (No synthetic data)

IMPORTANT DISCLAIMER:
This knowledge base contains ONLY information extracted directly from your provided documents.
No assumptions, estimates, or synthetic data have been added. If information seems incomplete,
it reflects the extractable content from the source PDF, not system limitations.

========================================================
EXTRACTED FEE INFORMATION
========================================================
"""
        
        if self.extracted_data['fee_information']:
            # Group fees by type
            fees_by_type = defaultdict(list)
            for fee in self.extracted_data['fee_information']:
                fees_by_type[fee['type']].append(fee)
            
            for fee_type, fees in fees_by_type.items():
                kb += f"\n{fee_type.upper().replace('_', ' ')} FEES:\n"
                for fee in fees:
                    kb += f"• ₹{fee['amount']} (Page {fee['page']}, Confidence: {fee['confidence']:.2f})\n"
                    kb += f"  Context: {fee['context'][:100]}...\n"
                kb += "\n"
        else:
            kb += "\nNo clear fee amounts were extractable from the provided document.\n"
            kb += "This may be due to:\n"
            kb += "• Fees presented in image/table format\n"
            kb += "• Complex document layout\n"
            kb += "• Text embedded in graphics\n\n"
        
        kb += """========================================================
EXTRACTED ACADEMIC PROGRAMS
========================================================
"""
        
        if self.extracted_data['academic_programs']:
            unique_programs = {}
            for program in self.extracted_data['academic_programs']:
                prog_name = program['program_name']
                if prog_name not in unique_programs:
                    unique_programs[prog_name] = program
            
            for program_name, program in unique_programs.items():
                kb += f"• {program_name} (Page {program['page']})\n"
            kb += "\n"
        else:
            kb += "No specific academic programs clearly identified in the extracted text.\n\n"
        
        kb += """========================================================
EXTRACTED CONTACT INFORMATION
========================================================
"""
        
        if self.extracted_data['contact_details']:
            contacts_by_type = defaultdict(list)
            for contact in self.extracted_data['contact_details']:
                contacts_by_type[contact['type']].append(contact)
            
            for contact_type, contacts in contacts_by_type.items():
                kb += f"\n{contact_type.upper()}:\n"
                for contact in contacts:
                    kb += f"• {contact['info']} (Page {contact['page']})\n"
            kb += "\n"
        else:
            kb += "No contact information clearly extractable from the document.\n\n"
        
        kb += """========================================================
EXTRACTED PLACEMENT INFORMATION
========================================================
"""
        
        if self.extracted_data['placement_info']:
            companies = set()
            packages = []
            
            for item in self.extracted_data['placement_info']:
                if 'company' in item:
                    companies.add(item['company'])
                if 'package' in item:
                    packages.append(item)
            
            if companies:
                kb += "Companies mentioned in placement context:\n"
                for company in sorted(companies):
                    kb += f"• {company}\n"
                kb += "\n"
            
            if packages:
                kb += "Package information found:\n"
                for pkg in packages:
                    kb += f"• {pkg['package']} (Page {pkg['page']})\n"
                kb += "\n"
        else:
            kb += "No placement information clearly extractable from the document.\n\n"
        
        kb += """========================================================
RAW EXTRACTED TEXT SAMPLES
========================================================

The following are samples of text extracted from each page:
"""
        
        for page_num, page_data in sorted(self.extracted_data['raw_pages'].items()):
            text_sample = page_data['combined_text'][:500] + "..." if len(page_data['combined_text']) > 500 else page_data['combined_text']
            kb += f"\n--- PAGE {page_num} SAMPLE ---\n"
            kb += f"Confidence Score: {page_data['confidence_score']:.2f}\n"
            kb += f"Text Length: {len(page_data['combined_text'])} characters\n"
            kb += f"Sample: {text_sample}\n"
        
        kb += """
========================================================
USAGE NOTES
========================================================

1. This knowledge base reflects ONLY what could be extracted from your PDF
2. No synthetic or assumed information has been added
3. If specific details are missing, they were not clearly extractable
4. For complete information, contact JECRC directly
5. Extraction confidence scores indicate OCR accuracy levels
6. Context snippets show surrounding text for verification

For official and complete information:
- Visit JECRC official website
- Contact the college directly
- Request current brochures/documents

========================================================
"""
        
        return kb
    
    def save_results(self, output_dir="documents/general"):
        """Save extraction results"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save knowledge base
        kb = self.generate_knowledge_base()
        kb_path = os.path.join(output_dir, "jecrc_college_info.txt")
        with open(kb_path, 'w', encoding='utf-8') as f:
            f.write(kb)
        
        # Save detailed extraction data as JSON
        json_path = os.path.join(output_dir, "jecrc_extraction_data.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.extracted_data, f, indent=2, ensure_ascii=False)
        
        return kb_path, json_path

def main():
    print("🚀 JECRC Real Document Extractor")
    print("=" * 60)
    print("🎯 Extracts ONLY genuine information from your actual PDF")
    print("❌ No synthetic data • No assumptions • No fabrication")
    print("✅ Only what's actually in your document")
    print("=" * 60)
    
    # Initialize extractor
    extractor = RealDocumentExtractor()
    
    # Define PDF path
    pdf_path = "documents/general/JECRC E-Brochure - 24-25.pdf"
    
    # Check if PDF exists
    if not os.path.exists(pdf_path):
        print(f"\n❌ PDF not found: {pdf_path}")
        print("📁 Please ensure your JECRC PDF is placed in: documents/general/")
        return
    
    print(f"\n📂 Found PDF: {pdf_path}")
    file_size = os.path.getsize(pdf_path) / (1024 * 1024)  # Size in MB
    print(f"📊 File size: {file_size:.2f} MB")
    
    # Process the document
    print(f"\n🔄 Starting real document extraction...")
    success = extractor.process_document(pdf_path)
    
    if success:
        # Save results
        kb_path, json_path = extractor.save_results()
        
        print(f"\n🎉 EXTRACTION SUCCESSFUL!")
        print(f"=" * 40)
        print(f"📝 Knowledge Base: {kb_path}")
        print(f"📊 Raw Data (JSON): {json_path}")
        print(f"💾 Knowledge Base Size: {len(extractor.generate_knowledge_base())} characters")
        
        # Show summary statistics
        stats = extractor.extracted_data['extraction_metadata']
        print(f"\n📈 EXTRACTION STATISTICS:")
        print(f"• Pages processed: {stats.get('pages_processed', 0)}/{stats.get('total_pages', 0)}")
        print(f"• Total text extracted: {stats.get('total_text_length', 0)} characters")
        print(f"• Fee information found: {len(extractor.extracted_data['fee_information'])} instances")
        print(f"• Academic programs: {len(extractor.extracted_data['academic_programs'])} found")
        print(f"• Contact details: {len(extractor.extracted_data['contact_details'])} found")
        print(f"• Placement references: {len(extractor.extracted_data['placement_info'])} found")
        
        print(f"\n🤖 NEXT STEPS:")
        print(f"1. Restart your RAG system to use the extracted information")
        print(f"2. The AI will now respond based ONLY on your actual document content")
        print(f"3. No more synthetic data - only genuine JECRC information!")
        
        if len(extractor.extracted_data['fee_information']) == 0:
            print(f"\n⚠️  FEE INFORMATION WARNING:")
            print(f"No clear fee amounts were found. This could mean:")
            print(f"• Fees are in table/image format (harder to extract)")
            print(f"• Complex layout with embedded graphics")
            print(f"• Fees mentioned in descriptive text rather than structured format")
        
    else:
        print(f"\n❌ EXTRACTION FAILED")
        print(f"This could be due to:")
        print(f"• PDF is password protected")
        print(f"• Document is entirely image-based")
        print(f"• Corrupted or unreadable PDF format")

if __name__ == "__main__":
    main()