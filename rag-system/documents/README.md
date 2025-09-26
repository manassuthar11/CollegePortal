# JECRC Foundation College Portal - Document Management System

## 📁 Document Organization Structure

The RAG system automatically processes documents placed in these categorized folders:

### 📋 **admissions/** 
- Admission procedures and requirements
- Eligibility criteria for different courses
- Application deadlines and important dates
- Entrance exam information
- Merit list and cutoff details
- Document verification requirements

**Supported file types:** PDF, DOCX, TXT

### 📚 **courses/**
- Course curriculum and syllabus
- Subject details and credit hours
- Faculty information
- Laboratory and practical details
- Course outcomes and objectives
- Semester-wise subject breakdown

**Supported file types:** PDF, DOCX, TXT

### 💰 **fees/**
- Fee structure for all courses
- Semester-wise fee breakdown
- Scholarship information
- Fee payment procedures and deadlines
- Refund policies
- Financial assistance details

**Supported file types:** PDF, DOCX, TXT

### 🏛️ **general/**
- College history and overview
- Campus facilities and infrastructure
- Rules and regulations
- Academic calendar
- Contact information
- Department details

**Supported file types:** PDF, DOCX, TXT

### 🏠 **hostel/**
- Accommodation facilities
- Hostel rules and regulations
- Room allocation procedures
- Mess and dining facilities
- Hostel fees and charges
- Safety and security measures

**Supported file types:** PDF, DOCX, TXT

### 💼 **placement/**
- Placement statistics and records
- Career guidance information
- Industry partnerships
- Training and skill development
- Alumni network details
- Job opportunities and internships

**Supported file types:** PDF, DOCX, TXT

### 📄 **forms/**
- Application forms
- Registration forms
- Fee payment forms
- Certificate request forms
- Leave application formats
- Other administrative forms

**Supported file types:** PDF, DOCX, TXT

## 🤖 How the RAG System Works

### 1. **Document Ingestion**
- Automatically scans all category folders
- Extracts text from PDF, DOCX, and TXT files
- Performs intelligent text cleaning and preprocessing
- Creates smart chunks with sentence awareness

### 2. **Vector Processing**
- Generates semantic embeddings using SentenceTransformers
- Stores vectors in ChromaDB for fast similarity search
- Creates TF-IDF index for keyword matching
- Implements hybrid search combining both approaches

### 3. **Query Processing**
- Understands natural language questions
- Performs semantic and keyword searches
- Ranks results by relevance and confidence
- Generates context-aware responses using DistilBERT

### 4. **Response Generation**
- Synthesizes information from multiple documents
- Provides source attribution and confidence scores
- Handles multi-document context assembly
- Delivers accurate, contextual answers

## 📤 Adding New Documents

### Simple Process:
1. **Place documents** in the appropriate category folder
2. **Supported formats:** PDF, DOCX, TXT
3. **Automatic processing** - The system will detect and process new files
4. **Immediate availability** - New information becomes searchable instantly

### Best Practices:
- **Use descriptive filenames** (e.g., "BTech_CSE_Admission_Requirements_2024.pdf")
- **Organize by category** to improve search accuracy
- **Keep documents updated** by replacing old versions
- **Use clear, well-formatted text** for better extraction

### Manual Reprocessing:
If you need to force reprocessing of all documents:
- Visit: http://localhost:8000
- Click the reprocess button, or
- Send POST request to `/reprocess` endpoint

## 🎯 Query Examples

The RAG system can answer questions like:

**Admissions:**
- "What are the eligibility criteria for B.Tech admission?"
- "When is the last date for application submission?"
- "What documents are required for admission?"

**Courses:**
- "Tell me about the Computer Science curriculum"
- "What subjects are taught in the first semester?"
- "Who are the faculty members in the Electronics department?"

**Fees:**
- "What is the fee structure for MBA program?"
- "Are there any scholarships available?"
- "How can I pay the semester fees?"

**Hostel:**
- "What are the hostel facilities available?"
- "How much does hostel accommodation cost?"
- "What are the hostel rules and regulations?"

**Placements:**
- "What is the placement record of the college?"
- "Which companies visit for campus recruitment?"
- "What training programs are available for placements?"

## 🔧 Technical Features

### Advanced Capabilities:
- **Multi-document synthesis** - Combines information from multiple sources
- **Confidence scoring** - Provides reliability estimates for answers
- **Source attribution** - Shows which documents were used
- **Context awareness** - Maintains conversation context
- **Hybrid search** - Semantic + keyword matching for better results

### Performance Optimizations:
- **Document caching** - Faster response times
- **Batch processing** - Efficient vector operations
- **Lazy loading** - Models loaded on demand
- **Memory management** - Optimized for local deployment

### Monitoring and Stats:
- Real-time knowledge base statistics
- Document processing status
- Query performance metrics
- System health monitoring

## 🚀 Getting Started

1. **Install Dependencies:**
   ```bash
   cd rag-system
   pip install -r requirements.txt
   ```

2. **Add Your Documents:**
   - Place PDF, DOCX, or TXT files in appropriate category folders
   - Documents will be processed automatically

3. **Start the System:**
   ```bash
   python smart_rag_app.py
   ```

4. **Access the Interface:**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/health

## 📊 System Requirements

- **Python:** 3.8 or higher
- **RAM:** 8GB recommended
- **Storage:** 2GB free space
- **Internet:** For initial model downloads

## 🆘 Troubleshooting

**Common Issues:**
- **No documents found:** Check if files are in correct category folders
- **Poor search results:** Ensure documents contain clear, readable text
- **Memory errors:** Reduce batch size or restart the system
- **Model download failures:** Check internet connection

**Support:**
- Check the application logs in `rag_system.log`
- Visit the `/stats` endpoint for system information
- Use the `/reprocess` endpoint to refresh the knowledge base

---

**🎓 JECRC Foundation Smart RAG Chatbot**  
*Intelligent College Information Assistant*  
*Version 1.0.0 - Advanced RAG System*