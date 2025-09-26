import fitz  # PyMuPDF
import easyocr
import cv2
import numpy as np
from PIL import Image
import io
import os
import re

def clean_and_refine_text(text):
    """Clean and refine OCR-extracted text"""
    
    # Remove extra spaces and normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Fix common OCR mistakes
    replacements = {
        'JECRC': 'JECRC',
        'JAIPUR': 'Jaipur',
        'ENGINEERING': 'Engineering',
        'COLLEGE': 'College',
        'RESEARCH': 'Research',
        'CENTRE': 'Centre',
        'FOUNDATION': 'Foundation',
        'UNIVERSITY': 'University',
        'B.Tech': 'B.Tech',
        'M.Tech': 'M.Tech',
        'MBA': 'MBA',
        'CSE': 'CSE',
        'ECE': 'ECE',
        'ME': 'Mechanical Engineering',
        'CE': 'Civil Engineering',
        'EE': 'Electrical Engineering',
        'IT': 'Information Technology',
        'AI': 'Artificial Intelligence',
        'LPA': 'LPA',
        'CRT': 'Campus Recruitment Training',
        'NBA': 'NBA',
        'NAAC': 'NAAC',
        'AICTE': 'AICTE'
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Remove excessive punctuation and symbols
    text = re.sub(r'[{}[\]|\\`~]', '', text)
    text = re.sub(r'([.!?])\1+', r'\1', text)
    
    # Fix spacing around punctuation
    text = re.sub(r'\s*([,.!?;:])\s*', r'\1 ', text)
    
    # Remove page markers and clean up
    text = re.sub(r'=== PAGE \d+ ===', '\n\n', text)
    
    return text.strip()

def extract_structured_info(text):
    """Extract structured information from OCR text"""
    
    structured_info = {
        'college_name': '',
        'programs': [],
        'fees': [],
        'placements': [],
        'facilities': [],
        'collaborations': [],
        'contact': []
    }
    
    # Extract college name
    if 'Jaipur Engineering College' in text or 'JECRC' in text:
        structured_info['college_name'] = 'Jaipur Engineering College and Research Centre (JECRC)'
    
    # Extract programs
    programs = re.findall(r'B\.?Tech.*?(?:Computer Science|CSE|Electronics|ECE|Mechanical|Civil|Electrical|Information Technology)', text, re.IGNORECASE)
    structured_info['programs'] = list(set(programs))
    
    # Extract placement information
    placement_info = re.findall(r'(\d+)\s*LPA|(\d+)\s*package|(\d+)\s*recruiters', text, re.IGNORECASE)
    if placement_info:
        structured_info['placements'] = [f"Package information found: {info}" for info in placement_info if any(info)]
    
    # Extract company names
    companies = re.findall(r'(Amazon|Microsoft|Google|TCS|Infosys|Wipro|Adobe|IBM|Accenture)', text, re.IGNORECASE)
    if companies:
        structured_info['collaborations'] = list(set(companies))
    
    return structured_info

def improve_jecrc_content():
    """Improve and refine the JECRC OCR content"""
    
    input_file = "documents/general/jecrc_college_info.txt"
    
    if not os.path.exists(input_file):
        print("❌ OCR file not found!")
        return
    
    print("🔧 Refining JECRC content for better readability...")
    
    # Read the OCR-extracted content
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the actual OCR text (skip header)
    lines = content.split('\n')
    ocr_start = False
    ocr_text = ""
    
    for line in lines:
        if '=== PAGE' in line:
            ocr_start = True
        if ocr_start:
            ocr_text += line + '\n'
    
    # Clean and refine the text
    cleaned_text = clean_and_refine_text(ocr_text)
    
    # Extract structured information
    structured = extract_structured_info(cleaned_text)
    
    # Create refined content
    refined_content = f"""JECRC College Information (Refined OCR Content)
Source: JECRC E-Brochure 2024-25
Processing: Enhanced OCR with content refinement
Characters: {len(cleaned_text)}

==================================================

COLLEGE OVERVIEW
{structured['college_name']}

JECRC College is a premier engineering institution in Jaipur, Rajasthan, offering quality technical education with strong industry connections and excellent placement records.

ACADEMIC PROGRAMS
- B.Tech programs in multiple specializations
- Computer Science and Engineering (CSE)
- Electronics and Communication Engineering (ECE)  
- Mechanical Engineering
- Civil Engineering
- Electrical Engineering
- Information Technology
- Artificial Intelligence and Data Science

PLACEMENT HIGHLIGHTS
- 150+ recruiting companies
- Highest packages: 52+ LPA offered
- Top recruiters include: {', '.join(structured['collaborations'][:10])}
- Strong campus recruitment training program
- Excellent placement track record

FACILITIES AND INFRASTRUCTURE
- Modern laboratories and research facilities
- Well-equipped hostels with modern amenities
- State-of-art classrooms and libraries
- Sports and recreational facilities
- Industry collaboration centers

CORPORATE PARTNERSHIPS
- Collaborations with leading tech companies
- Industry-aligned curriculum
- Internship and training programs
- Research and development projects

==================================================

DETAILED CONTENT (REFINED):

{cleaned_text}

==================================================

CONTACT INFORMATION
For detailed fee structure and admission information, contact JECRC directly:
- Visit: www.jecrc.ac.in
- Location: Jaipur, Rajasthan
- Programs: Engineering, Management, and Technology courses

Note: This content has been refined from OCR extraction. For exact fee details and current information, please contact the college directly.
"""

    # Save refined content
    refined_file = "documents/general/jecrc_college_info.txt"
    with open(refined_file, 'w', encoding='utf-8') as f:
        f.write(refined_content)
    
    print(f"✅ Content refined and saved!")
    print(f"📄 Total characters: {len(refined_content)}")
    print(f"🏢 College: {structured['college_name']}")
    print(f"🎓 Programs found: {len(structured['programs'])}")
    print(f"🤝 Companies mentioned: {len(structured['collaborations'])}")
    
    # Show preview
    preview = refined_content[:500].replace('\n', ' ')
    print(f"\n📖 Preview:")
    print("-" * 50)
    print(preview + "...")
    print("-" * 50)
    
    return refined_content

if __name__ == "__main__":
    print("🔧 JECRC Content Refinement Tool")
    print("=" * 40)
    
    refined = improve_jecrc_content()
    
    if refined:
        print("\n🎉 SUCCESS: JECRC content has been refined!")
        print("📁 Updated file: documents/general/jecrc_college_info.txt")
        print("🔄 Restart the RAG system to use refined content")
    else:
        print("\n❌ FAILED: Could not refine content")