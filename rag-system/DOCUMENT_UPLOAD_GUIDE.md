# 📁 DOCUMENT UPLOAD GUIDE
## How to Add Your Own Documents to the RAG System

### 🗂️ **Available Document Categories:**

Place your documents in these folders based on content type:

```
📁 rag-system/documents/
├── 📋 admissions/     ← Admission procedures, eligibility, deadlines
├── 📚 courses/        ← Course details, curriculum, syllabus  
├── 💰 fees/          ← Fee structure, payment info, scholarships
├── 🏛️ general/        ← College info, facilities, rules
├── 🏠 hostel/         ← Accommodation, hostel facilities
├── 💼 placement/      ← Career services, job placements
└── 📄 forms/          ← Application forms, documents
```

### 📄 **Supported File Types:**

✅ **PDF Files** (.pdf)
- Admission brochures
- Course catalogs  
- Fee structures
- Official documents

✅ **Word Documents** (.docx)
- Policies and procedures
- Detailed information sheets
- Faculty information

✅ **Text Files** (.txt)
- Simple information files
- FAQ documents
- Quick reference guides

### 🚀 **How to Add Documents:**

1. **Choose the Right Category**
   - Look at your document content
   - Select the most appropriate folder
   - Example: Fee receipts → `fees/` folder

2. **Copy Your Files**
   - Simply copy/paste your documents
   - Into the appropriate category folder
   - No special naming required (but descriptive names help)

3. **Automatic Processing**
   - The RAG system automatically detects new files
   - Processes them when you start the application
   - Creates searchable knowledge base

4. **Start the System**
   ```bash
   cd rag-system
   python smart_rag_app.py
   ```

### 📸 **For Images/Photos:**

**Note:** The current system processes text-based documents. For images containing text:

**Option 1 - Convert to PDF:**
- Scan/photograph documents to PDF
- Use phone apps like CamScanner
- Place PDF in appropriate folder

**Option 2 - OCR Conversion:**
- Use OCR software to extract text
- Save as TXT or DOCX file
- Upload the text version

### 📝 **Document Quality Tips:**

**For Best Results:**
- ✅ Clear, readable text
- ✅ Well-formatted documents
- ✅ Descriptive filenames
- ✅ Organized by category

**Avoid:**
- ❌ Scanned images with poor quality
- ❌ Password-protected PDFs
- ❌ Corrupted files
- ❌ Non-text content only

### 🔄 **After Adding Documents:**

1. **Start the RAG System:**
   ```bash
   python smart_rag_app.py
   ```

2. **Check Processing Status:**
   - Visit: http://localhost:8000
   - View document statistics
   - Confirm your files are loaded

3. **Test with Queries:**
   - Ask questions about your documents
   - Check if responses use your content
   - Verify source attribution

### 🛠️ **Troubleshooting:**

**Documents Not Found:**
- Check file extensions (.pdf, .docx, .txt)
- Verify files are in correct category folders
- Restart the application

**Poor Search Results:**
- Ensure documents contain readable text
- Check for text extraction errors
- Try simpler, more specific queries

**Processing Errors:**
- Check application logs: `rag_system.log`
- Verify file permissions
- Ensure files aren't corrupted

### 🔍 **Example Document Organization:**

```
📁 admissions/
├── BTech_Admission_2024.pdf
├── Eligibility_Criteria.docx
└── Application_Process.txt

📁 courses/
├── CSE_Curriculum.pdf
├── Faculty_List.docx
└── Lab_Details.txt

📁 fees/
├── Fee_Structure_2024.pdf
├── Scholarship_Info.docx
└── Payment_Methods.txt
```

### 🎯 **Ready to Use!**

Once you've added your documents:

1. **Documents are automatically processed**
2. **Knowledge base is created**
3. **RAG system is ready for queries**
4. **Ask questions about your specific content**

The system will intelligently search through YOUR documents and provide accurate answers with source attribution!

---
**📞 Need Help?** Check the main README.md or application logs for troubleshooting.