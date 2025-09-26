"""
Simple College Browser RAG System
A lightweight version for immediate use
"""
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import PyPDF2
import json

app = Flask(__name__)
CORS(app)

# Simple document storage
documents = {}

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>College Portal - RAG System</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 {
            color: #4f46e5;
            text-align: center;
            margin-bottom: 30px;
        }
        .chat-container {
            border: 2px solid #e5e7eb;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            height: 400px;
            overflow-y: auto;
            background: #f9fafb;
        }
        .input-container {
            display: flex;
            gap: 10px;
        }
        input[type="text"] {
            flex: 1;
            padding: 12px;
            border: 2px solid #d1d5db;
            border-radius: 8px;
            font-size: 16px;
        }
        button {
            padding: 12px 24px;
            background: #4f46e5;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
        }
        button:hover {
            background: #4338ca;
        }
        .message {
            margin-bottom: 15px;
            padding: 10px 15px;
            border-radius: 10px;
        }
        .user-message {
            background: #dbeafe;
            margin-left: 20%;
            text-align: right;
        }
        .bot-message {
            background: #f3f4f6;
            margin-right: 20%;
        }
        .status {
            text-align: center;
            padding: 20px;
            background: #ecfdf5;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .upload-info {
            background: #fef3c7;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎓 College Portal - AI Assistant</h1>
        
        <div class="status">
            <h3>📁 Document Status</h3>
            <p id="docStatus">Ready to process your college documents!</p>
        </div>

        <div class="upload-info">
            <h3>📤 How to Add Your College Browser PDF:</h3>
            <p><strong>1.</strong> Copy your college browser PDF to: <code>documents/general/</code></p>
            <p><strong>2.</strong> Refresh this page</p>
            <p><strong>3.</strong> Ask questions about your college!</p>
        </div>
        
        <div class="chat-container" id="chatContainer">
            <div class="bot-message message">
                <strong>AI Assistant:</strong> Hello! I'm ready to help you with college information. Upload your college browser PDF to the documents/general/ folder and ask me anything about your college!
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="userInput" placeholder="Ask me about your college..." onkeypress="handleEnter(event)">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        function handleEnter(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Display user message
            addMessage(message, 'user');
            input.value = '';
            
            // Send to backend
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                addMessage(data.response, 'bot');
            })
            .catch(error => {
                addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            });
        }
        
        function addMessage(message, sender) {
            const chatContainer = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            messageDiv.innerHTML = `<strong>${sender === 'user' ? 'You' : 'AI Assistant'}:</strong> ${message}`;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        // Check document status on load
        fetch('/status')
        .then(response => response.json())
        .then(data => {
            document.getElementById('docStatus').textContent = data.status;
        });
    </script>
</body>
</html>
"""

def load_documents():
    """Load documents from the documents folder"""
    # Ensure we're in the right directory
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    documents_path = "documents"
    
    if not os.path.exists(documents_path):
        return "No documents folder found"
    
    doc_count = 0
    total_files = 0
    
    for root, dirs, files in os.walk(documents_path):
        for file in files:
            total_files += 1
            if file.endswith('.pdf'):
                file_path = os.path.join(root, file)
                print(f"Processing PDF: {file_path}")
                try:
                    text_content = extract_pdf_text(file_path)
                    if text_content and not text_content.startswith("Error") and len(text_content.strip()) > 10:
                        documents[file] = text_content
                        doc_count += 1
                        print(f"Successfully loaded {file} - {len(text_content)} characters")
                    else:
                        print(f"Failed to extract text from {file}: {text_content}")
                except Exception as e:
                    print(f"Error processing {file}: {e}")
            elif file.endswith('.txt'):
                file_path = os.path.join(root, file)
                print(f"Processing TXT: {file_path}")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text_content = f.read()
                        documents[file] = text_content
                        doc_count += 1
                        print(f"Successfully loaded {file} - {len(text_content)} characters")
                except Exception as e:
                    print(f"Error processing {file}: {e}")
            elif file.endswith('.docx'):
                print(f"Found docx file: {file} (not yet implemented)")
                # Could add docx support later
    
    result = f"Loaded {doc_count} documents out of {total_files} total files"
    print(result)
    
    # Debug: Print first 200 characters of each document
    for doc_name, content in documents.items():
        preview = content[:200].replace('\n', ' ')
        print(f"Document '{doc_name}' preview: {preview}...")
    
    return result

def extract_pdf_text(pdf_path):
    """Extract text from PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            page_count = len(pdf_reader.pages)
            print(f"PDF has {page_count} pages")
            
            for i, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                        print(f"Page {i+1}: extracted {len(page_text)} characters")
                    else:
                        print(f"Page {i+1}: no text extracted")
                except Exception as e:
                    print(f"Error extracting page {i+1}: {e}")
            
            if text.strip():
                return text
            else:
                return "Error: No text could be extracted from PDF"
                
    except Exception as e:
        return f"Error reading PDF: {e}"

def simple_search(query, documents):
    """Simple keyword-based search"""
    query_lower = query.lower()
    results = []
    
    # Enhanced keyword mapping
    fee_keywords = ['fee', 'fees', 'cost', 'tuition', 'payment', 'money', 'price', 'amount']
    college_keywords = ['college', 'university', 'institution', 'school', 'name']
    department_keywords = ['department', 'departments', 'faculty', 'course', 'courses', 'program', 'programs']
    
    # Check what type of query this is
    if any(keyword in query_lower for keyword in fee_keywords):
        search_terms = fee_keywords + query_lower.split()
    elif any(keyword in query_lower for keyword in college_keywords):
        search_terms = college_keywords + query_lower.split()
    elif any(keyword in query_lower for keyword in department_keywords):
        search_terms = department_keywords + query_lower.split()
    else:
        search_terms = query_lower.split()
    
    print(f"Searching for: {search_terms}")
    
    for doc_name, content in documents.items():
        content_lower = content.lower()
        # More flexible matching
        matched_terms = []
        for term in search_terms:
            if term in content_lower:
                matched_terms.append(term)
        
        if matched_terms:
            print(f"Found matches for: {matched_terms} in {doc_name}")
            # Find relevant sentences
            sentences = content.split('.')
            relevant = []
            for sentence in sentences:
                sentence_lower = sentence.lower()
                if any(term in sentence_lower for term in matched_terms):
                    clean_sentence = sentence.strip()
                    if len(clean_sentence) > 10:  # Only meaningful sentences
                        relevant.append(clean_sentence)
            
            if relevant:
                # Limit to most relevant sentences
                top_relevant = relevant[:5]
                results.append(f"From {doc_name}:\n" + "\n".join(top_relevant))
    
    print(f"Search results: {len(results)} matches found")
    return results

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/status')
def status():
    doc_status = load_documents()
    return jsonify({
        'status': doc_status,
        'document_count': len(documents)
    })

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not documents:
        load_documents()
    
    if not documents:
        return jsonify({
            'response': "I don't have any documents loaded yet. Please upload your college browser PDF to the documents/general/ folder and refresh the page."
        })
    
    # Simple search and response
    results = simple_search(user_message, documents)
    
    if results:
        response = "Based on your college documents:\n\n" + "\n\n".join(results[:2])
    else:
        response = "I couldn't find specific information about that in your college documents. Try asking about facilities, admissions, courses, or general college information."
    
    return jsonify({'response': response})

if __name__ == '__main__':
    print("🎓 College Portal RAG System Starting...")
    print("📁 Place your college browser PDF in: documents/general/")
    print("🌐 Open your browser to: http://localhost:8000")
    print("✨ Ready to answer questions about your college!")
    
    # Load documents at startup
    print("\n📚 Loading college documents...")
    result = load_documents()
    print(f"✅ {result}")
    
    app.run(host='0.0.0.0', port=8000, debug=True)